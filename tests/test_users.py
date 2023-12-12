import http
from uuid import UUID

from starlette.testclient import TestClient

from common import ObjRef
from enums import SortOrder
from logic.users import User, RetrievedProfile, RetrievedUser, ProfileUpdate
from logic.users.business import Profile


def test_retrieve_non_existent_user(client: TestClient):
    get_res = client.get("/users/9515d9bb-d4d6-4952-9003-9d7e0436fe58")
    assert get_res.status_code == http.HTTPStatus.NOT_FOUND
    content = get_res.json()
    assert content["detail"] == 'User not found. ID: 9515d9bb-d4d6-4952-9003-9d7e0436fe58'


def test_user_flow(client: TestClient):
    user = User.model_validate(dict(email="someemail@gmail.com"))
    res = client.post("/users", data=user.model_dump_json())
    assert res.status_code == http.HTTPStatus.CREATED

    user_id = ObjRef.model_validate(res.json()).id

    get_res = client.get(f"/users/{user_id}")

    assert get_res.status_code == http.HTTPStatus.OK
    user = User.model_validate(get_res.json())
    assert user.email_is("someemail@gmail.com")

    update_data = User.model_validate({"email": "newemail@gmail.com"})
    update_res = client.patch(f"/users/{user_id}", data=update_data.model_dump_json())
    assert update_res.status_code == http.HTTPStatus.NO_CONTENT

    get_res = client.get(f"/users/{user_id}")
    user = RetrievedUser.model_validate(get_res.json())
    assert user.email_is("newemail@gmail.com")

    delete_res = client.delete(f"/users/{user_id}")
    assert delete_res.status_code == http.HTTPStatus.NO_CONTENT

    get_res = client.get(f"/users/{user_id}")
    assert get_res.status_code == http.HTTPStatus.NOT_FOUND
    content = get_res.json()
    assert content["detail"] == f'User not found. ID: {user_id}'


def test_profile_flow(client: TestClient, user: [UUID, User]):
    user_id, user = user
    profile = Profile.model_validate({'full_name': "My full name", 'description': "Hey there!"})
    res_post = client.post(f"/users/{user_id}/profiles", data=profile.model_dump_json())
    assert res_post.status_code == http.HTTPStatus.CREATED
    profile_id = ObjRef.model_validate(res_post.json()).id
    get_res = client.get(f"/profiles/{profile_id}")
    assert get_res.status_code == http.HTTPStatus.OK
    profile_a = RetrievedProfile.model_validate(get_res.json())
    assert profile_a.is_named("My full name")
    assert profile_a.is_described_as("Hey there!")
    assert not profile_a.is_favorite

    profile = Profile.model_validate({'full_name': "My full name from another profile",
                                      'description': "Hello there!", "is_favorite": True})
    res_post = client.post(f"/users/{user_id}/profiles", data=profile.model_dump_json())
    assert res_post.status_code == http.HTTPStatus.CREATED
    profile_id = ObjRef.model_validate(res_post.json()).id
    get_res = client.get(f"/profiles/{profile_id}")
    assert get_res.status_code == http.HTTPStatus.OK
    profile_b = RetrievedProfile.model_validate(get_res.json())
    assert profile_b.is_named("My full name from another profile")
    assert profile_b.is_described_as("Hello there!")
    assert profile_b.is_favorite

    res_get_list = client.get(f"/users/{user_id}/profiles")
    assert res_get_list.status_code == http.HTTPStatus.OK
    list_content = res_get_list.json()
    assert len(list_content) == 2
    ids = [UUID(d['id']) for d in list_content]
    assert profile_a.id in ids
    assert profile_b.id in ids


    update_payload = ProfileUpdate.model_validate({"description": "new description"})
    update_res = client.patch(f"/profiles/{profile_a.id}", data=update_payload.model_dump_json())
    assert update_res.status_code == http.HTTPStatus.NO_CONTENT
    get_res = client.get(f"/profiles/{profile_a.id}")
    profile_a_updated = RetrievedProfile.model_validate(get_res.json())
    assert profile_a_updated.is_named("My full name")
    assert profile_a_updated.is_described_as("new description")
    assert not profile_a_updated.is_favorite


    delete_res = client.delete(f"/profiles/{profile_a.id}")
    assert delete_res.status_code == http.HTTPStatus.NO_CONTENT
    get_res = client.get(f"/profiles/{profile_a.id}")
    assert get_res.status_code == http.HTTPStatus.NOT_FOUND
