from qna_api.features.user.models import SignupResponse, User

mock_user = User(
    id=1,
    username="testuser",
    email="testuser@example.com",
    full_name="Test User",
    disabled=False
)

mock_new_user = SignupResponse(
    user=User(
        id=2,
        username="newuser",
        email="newuser@example.com",
        full_name="New User",
        password="password123",
    ),
    message="User created successfully"
)

mock_updated_user = User(
    id=1,
    username="updateduser",
    email="updateduser@example.com",
    full_name="Updated User",
    password="password123"
)

