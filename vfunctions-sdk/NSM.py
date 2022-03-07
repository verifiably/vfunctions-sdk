import aws_nsm_interface
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class NSM():
    def __init__(self):
        self._nsm_dev = aws_nsm_interface.open_nsm_device()
        # Generate key pair
        self.nsm_rand_func = lambda num_bytes : aws_nsm_interface.get_random(
                self._nsm_dev, num_bytes)

        self._monkey_patch_crypto(self.nsm_rand_func)

        self._rsa_key = RSA.generate(2048)
        self._public_key = self._rsa_key.publickey().export_key('DER')

    def get_attestation_doc(self, public_key=None, user_data=None, nonce=None):
        attestation_doc = aws_nsm_interface.get_attestation_doc(
            self._nsm_dev,
            public_key = public_key,
            user_data = user_data,
            nonce = nonce
        )['document']

        return attestation_doc

    def decrypt(self, cipherdata):
        cipher = PKCS1_OAEP.new(self._rsa_key)
        plaintext = cipher.decrypt(cipherdata)

        return plaintext.decode()

    @classmethod
    def _monkey_patch_crypto(cls, nsm_rand_func):
        """Monkeypatch Crypto to use the NSM rand function."""
        Crypto.Random.get_random_bytes = nsm_rand_func
        def new_random_read(self, n_bytes): # pylint:disable=unused-argument
            return nsm_rand_func(n_bytes)
        Crypto.Random._UrandomRNG.read = new_random_read # pylint:disable=protected-access
