def test_create_prompt_with_tags(client):
    response = client.post(
        "/prompts",
        json={
            "title": "Test Prompt",
            "body": "Test Content",
            "category": "Test Category",
            "tags": ["tag1", "tag2"],
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Prompt"
    assert {tag["name"] for tag in data["tags"]} == {"tag1", "tag2"}


def test_filter_by_tag(client):
    client.post(
        "/prompts",
        json={
            "title": "Prompt 1",
            "body": "Content 1",
            "category": "Category 1",
            "tags": ["tag1"],
        },
    )
    client.post(
        "/prompts",
        json={
            "title": "Prompt 2",
            "body": "Content 2",
            "category": "Category 2",
            "tags": ["tag2"],
        },
    )
    response = client.get("/prompts", params={"tag": "tag1"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert {tag["name"] for tag in data[0]["tags"]} == {"tag1"}


def test_update_tags(client):
    response = client.post(
        "/prompts",
        json={
            "title": "Prompt 1",
            "body": "Content 1",
            "category": "Category 1",
            "tags": ["tag1"],
        },
    )
    assert response.status_code == 201
    prompt_id = response.json()["id"]

    response = client.patch(
        f"/prompts/{prompt_id}",
        json={
            "tags": ["tag2", "tag3"]
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert {tag["name"] for tag in data["tags"]} == {"tag2", "tag3"}


def test_update_without_tags_keeps_them(client):
    response = client.post(
        "/prompts",
        json={
            "title": "Prompt 1",
            "body": "Content 1",
            "category": "Category 1",
            "tags": ["tag1"],
        },
    )
    assert response.status_code == 201
    prompt_id = response.json()["id"]

    response = client.patch(
        f"/prompts/{prompt_id}",
        json={
            "title": "Updated Prompt 1"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Prompt 1"
    assert {tag["name"] for tag in data["tags"]} == {"tag1"}