from app.models.user import User
from app.utils.auth import hash_password


def register(c, name="alice", **extra):
    return c.post("/api/auth/register", json={"email": f"{name}@example.com", "username": name,
                                              "password": "correct-horse", **extra})


def login(c, name="alice", password="correct-horse"):
    return c.post("/api/auth/login", data={"username": name, "password": password})


def test_health(client):
    c, _ = client
    assert c.get("/api/health").json() == {"status": "ok"}


def test_register_and_login(client):
    c, _ = client
    r = register(c)
    assert r.status_code == 200 and r.json()["is_admin"] is False
    token = login(c).json()["access_token"]
    assert token.count(".") == 2
    assert login(c, password="wrong").status_code == 401


def test_registration_cannot_grant_admin(client):
    c, _ = client
    assert register(c, "mallory", is_admin=True).json()["is_admin"] is False


def test_duplicates_and_weak_passwords_rejected(client):
    c, _ = client
    register(c)
    assert register(c).status_code == 400
    assert c.post("/api/auth/register", json={"email": "b@example.com", "username": "bob", "password": "short"}).status_code == 422


def test_admin_routes_need_an_admin(client):
    c, Session = client
    register(c)
    user_token = login(c).json()["access_token"]
    assert c.get("/api/admin/users", headers={"Authorization": f"Bearer {user_token}"}).status_code == 403
    assert c.get("/api/admin/users").status_code == 401
    with Session() as db:
        db.add(User(email="root@example.com", username="root", hashed_password=hash_password("correct-horse"), is_admin=True))
        db.commit()
    admin_token = login(c, "root").json()["access_token"]
    r = c.get("/api/admin/users", headers={"Authorization": f"Bearer {admin_token}"})
    assert r.status_code == 200


def test_tampered_token_is_rejected(client):
    c, _ = client
    register(c)
    token = login(c).json()["access_token"]
    bad = token[:-2] + ("AA" if not token.endswith("AA") else "BB")
    assert c.get("/api/admin/users", headers={"Authorization": f"Bearer {bad}"}).status_code == 401


def test_admin_search_works(client):
    c, Session = client
    with Session() as db:
        db.add(User(email="root@example.com", username="root", hashed_password=hash_password("correct-horse"), is_admin=True))
        db.commit()
    register(c, "alice")
    token = login(c, "root").json()["access_token"]
    r = c.get("/api/admin/users?search=ali", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200 and "alice" in r.text and "root" not in r.text.replace("root@", "")
