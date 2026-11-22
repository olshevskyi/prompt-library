prompt = {
  "title": '',
  "body": '',
  "tags": [],
  "category": '',
  "is_favorite": False
}

print(f"Prompt: {prompt['title']} [{prompt['category']}]")

prompts = [
  {
    "title": 'test 1',
    "body": 'testing prompt',
    "tags": ['test'],
    "category": 'technical',
    "is_favorite": True
  },
  {
    "title": 'test 2',
    "body": 'another test prompt',
    "tags": ['test', 'example'],
    "category": 'general',
    "is_favorite": False
  },
  {
    "title": 'test 3',
    "body": 'yet another test prompt',
    "tags": ['test', 'sample'],
    "category": 'general',
    "is_favorite": False
  }
]

for prompt in prompts:
  if prompt["is_favorite"]:
    print(prompt["title"])

def find_by_category(prompts: list, category: str) -> list[dict]:
  return [prompt for prompt in prompts if prompt["category"] == category]

def all_tags(prompts: list) -> set[str]:
  tags = set()
  for prompt in prompts:
    tags.update(prompt["tags"])
  return tags

def render(body: str, variables: dict[str, str]) -> str:
  for key, value in variables.items():
    body = body.replace(f"{{{{{key}}}}}", value)
  return body

def get_prompt(prompts: list[dict], index: int) -> dict:
  return prompts[index]

try:
  print(get_prompt(prompts, 10))
except IndexError:
  print("Prompt not found.")

