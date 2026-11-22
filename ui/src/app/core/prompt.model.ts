// Mirrors the Pydantic schemas in prompt_api/app/schemas.py

export interface Tag {
  id: number;
  name: string;
}

/** PromptRead: what the API returns */
export interface Prompt {
  id: number;
  title: string;
  body: string;
  category: string;
  tags: Tag[];
  is_favorite: boolean;
  created_at: string;
  updated_at: string;
}

/** PromptCreate: body of POST /prompts */
export interface PromptCreate {
  title: string;
  body: string;
  category: string;
  tags: string[];
  is_favorite: boolean;
}

/** PromptUpdate: body of PATCH /prompts/{id}, every field optional */
export type PromptUpdate = Partial<PromptCreate>;

/** Query params of GET /prompts */
export interface PromptFilters {
  category?: string;
  favorite?: boolean;
  tag?: string;
}
