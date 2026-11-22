def test_create_prompt(client):
    response = client.post(
        "/prompts",
        json={
            "title": "Test Prompt",
            "body": "Test Content",
            "category": "Test Category",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Prompt"
    assert data["body"] == "Test Content"
    assert data["category"] == "Test Category"
    assert data["is_favorite"] is False
    assert "id" in data


def test_create_prompt_empty_title(client):
    response = client.post(
        "/prompts",
        json={"title": "", "body": "Test Content", "category": "Test Category"},
    )
    assert response.status_code == 422


def test_list_prompts(client):
    # Create two prompts to ensure there is at least one prompt in the list
    client.post(
        "/prompts",
        json={
            "title": "Test Prompt 1",
            "body": "Test Content 1",
            "category": "Test Category 1",
        },
    )
    client.post(
        "/prompts",
        json={
            "title": "Test Prompt 2",
            "body": "Test Content 2",
            "category": "Test Category 2",
        },
    )
    response = client.get("/prompts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_prompt_not_found(client):
    response = client.get("/prompts/999999")
    assert response.status_code == 404


def test_update_favorite(client):
    # Create a prompt to update its favorite status
    response = client.post(
        "/prompts",
        json={
            "title": "Test Prompt",
            "body": "Test Content",
            "category": "Test Category",
        },
    )
    assert response.status_code == 201
    data = response.json()
    prompt_id = data["id"]

    # Update the favorite status
    response = client.patch(f"/prompts/{prompt_id}", json={"is_favorite": True})
    assert response.status_code == 200
    data = response.json()
    assert data["is_favorite"] is True
    assert data["title"] == "Test Prompt"


def test_update_null_title(client):
    # Create a prompt to update its title to null
    response = client.post(
        "/prompts",
        json={
            "title": "Test Prompt",
            "body": "Test Content",
            "category": "Test Category",
        },
    )
    assert response.status_code == 201
    data = response.json()
    prompt_id = data["id"]

    # Attempt to update the title to null
    response = client.patch(f"/prompts/{prompt_id}", json={"title": None})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Prompt"


def test_delete_prompt(client):
    # Create a prompt to delete
    response = client.post(
        "/prompts",
        json={
            "title": "Test Prompt",
            "body": "Test Content",
            "category": "Test Category",
        },
    )
    assert response.status_code == 201
    data = response.json()
    prompt_id = data["id"]

    # Delete the prompt
    response = client.delete(f"/prompts/{prompt_id}")
    assert response.status_code == 204

    # Verify the prompt is deleted
    response = client.get(f"/prompts/{prompt_id}")
    assert response.status_code == 404


def test_filter_favorite(client):
    # Create two prompts, one favorite and one not
    response = client.post(
        "/prompts",
        json={
            "title": "Favorite Prompt",
            "body": "Test Content",
            "category": "Test Category",
            "is_favorite": True,
        },
    )
    assert response.status_code == 201

    response = client.post(
        "/prompts",
        json={
            "title": "Non-Favorite Prompt",
            "body": "Test Content",
            "category": "Test Category",
        },
    )
    assert response.status_code == 201

    # Filter favorite prompts
    response = client.get("/prompts?favorite=true")
    assert response.status_code == 200
    data = response.json()
    assert all(prompt["is_favorite"] is True for prompt in data)
