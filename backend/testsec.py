from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token
)

password = "Password@123"

hashed = hash_password(password)

print("Hashed Password:")
print(hashed)

print()

print("Verify:")
print(verify_password(password, hashed))

print()

token = create_access_token(
    subject="123",
    organization_id="456",
    role="ADMIN"
)

print("JWT:")
print(token)

print()

print("Decoded:")
print(decode_token(token))