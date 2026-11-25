NEW_ITEM = {"name": "Bánh mì pate", "category": "an_vat", "price": 15000}


# ---------- Đọc dữ liệu (công khai) ----------
def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_list_public_has_4_items(client):
    r = client.get("/menu-items")
    assert r.status_code == 200 and len(r.json()) == 4


def test_filter_unavailable(client):
    r = client.get("/menu-items?available=false")
    assert [i["name"] for i in r.json()] == ["Bánh đa cua"]


def test_get_not_found_and_invalid_id(client):
    assert client.get("/menu-items/999").status_code == 404
    assert client.get("/menu-items/0").status_code == 422


# ---------- Đăng nhập ----------
def test_login_wrong_password(client):
    r = client.post("/auth/login",
                    data={"username": "admin", "password": "abc"})
    assert r.status_code == 401


def test_login_ok_returns_token(client):
    r = client.post("/auth/login",
                    data={"username": "admin", "password": "admin123"})
    assert r.status_code == 200
    assert r.json()["token_type"] == "bearer"


# ---------- Bảo vệ endpoint ghi ----------
def test_write_without_token_is_401(client):
    assert client.post("/menu-items", json=NEW_ITEM).status_code == 401
    assert client.delete("/menu-items/1").status_code == 401


def test_write_with_invalid_token_is_401(client):
    h = {"Authorization": "Bearer token-gia"}
    assert client.post("/menu-items", json=NEW_ITEM,
                       headers=h).status_code == 401


def test_student_cannot_write_is_403(client, student):
    assert client.post("/menu-items", json=NEW_ITEM,
                       headers=student).status_code == 403
    assert client.delete("/menu-items/1",
                         headers=student).status_code == 403


def test_student_can_still_read(client, student):
    assert client.get("/menu-items", headers=student).status_code == 200


# ---------- CRUD với quyền nhân viên ----------
def test_create_201_with_location(client, staff):
    r = client.post("/menu-items", json=NEW_ITEM, headers=staff)
    assert r.status_code == 201
    assert r.headers["Location"] == f"/menu-items/{r.json()['id']}"
    assert r.json()["available"] is True


def test_create_duplicate_name_409(client, staff):
    client.post("/menu-items", json=NEW_ITEM, headers=staff)
    dup = {**NEW_ITEM, "name": "BÁNH MÌ PATE"}
    assert client.post("/menu-items", json=dup,
                       headers=staff).status_code == 409


def test_create_invalid_data_422(client, staff):
    bad_cases = [
        {**NEW_ITEM, "price": 30500},      # không là bội số 1000
        {**NEW_ITEM, "price": -5000},      # giá âm
        {**NEW_ITEM, "price": 250000},     # quá 200000
        {**NEW_ITEM, "category": "lau"},   # sai loại
        {**NEW_ITEM, "name": "   "},       # tên toàn dấu cách
    ]
    for body in bad_cases:
        r = client.post("/menu-items", json=body, headers=staff)
        assert r.status_code == 422, body


def test_name_is_stripped(client, staff):
    r = client.post("/menu-items", headers=staff,
                    json={**NEW_ITEM, "name": "  Bánh mì pate  "})
    assert r.json()["name"] == "Bánh mì pate"


def test_put_replaces_item(client, staff):
    body = {"name": "Trà đào", "category": "do_uong", "price": 20000,
            "available": True}
    r = client.put("/menu-items/4", json=body, headers=staff)
    assert r.status_code == 200 and r.json()["price"] == 20000


def test_patch_only_changes_sent_field(client, staff):
    r = client.patch("/menu-items/2", json={"available": False},
                     headers=staff)
    assert r.status_code == 200
    assert r.json()["available"] is False
    assert r.json()["price"] == 30000  # giữ nguyên


def test_patch_duplicate_name_409(client, staff):
    r = client.patch("/menu-items/1", json={"name": "trà chanh"},
                     headers=staff)
    assert r.status_code == 409


def test_delete_then_404(client, staff):
    assert client.delete("/menu-items/1", headers=staff).status_code == 204
    assert client.get("/menu-items/1").status_code == 404
    assert client.delete("/menu-items/1", headers=staff).status_code == 404
