import secrets
import hashlib

class Security:
    @staticmethod
    def generate_secure_id() -> str:
        """Gera um ID aleatório seguro para sessões ou arquivos temporários."""
        return secrets.token_urlsafe(16)

    @staticmethod
    def get_file_hash(content: bytes) -> str:
        """Gera um hash SHA256 do arquivo para evitar processar o mesmo arquivo várias vezes."""
        return hashlib.sha256(content).hexdigest()