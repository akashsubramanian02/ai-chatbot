from auth.auth_manager import (
    register_user,
    login_user
)

print(
    register_user(
        "akash",
        "akash@gmail.com",
        "12345"
    )
)

print(
    login_user(
        "akash",
        "12345"
    )
)