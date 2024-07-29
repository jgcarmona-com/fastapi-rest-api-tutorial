from qna_api.user.models import User, UserCreate, UserUpdate

# Define some mock data
mock_user = User(
    id=1,
    username="testuser",
    email="testuser@example.com",
    full_name="Test User",
    disabled=False
)

mock_user_create = UserCreate(
    username="newuser",
    email="newuser@example.com",
    full_name="New User",
    password="password123"
)

mock_user_update = UserUpdate(
    username="updateduser",
    email="updateduser@example.com",
    full_name="Updated User"
)

mock_updated_user = mock_user.model_copy()
mock_updated_user.username = "updateduser"
mock_updated_user.email = "updateduser@example.com"
mock_updated_user.full_name = "Updated User"
mock_updated_user.disabled = False
