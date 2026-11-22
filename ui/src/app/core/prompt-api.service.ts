import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { Prompt, PromptCreate, PromptFilters, PromptUpdate } from './prompt.model';

// "/api" is proxied to http://127.0.0.1:8000 by proxy.conf.json
const API = '/api/prompts';

/** One method per endpoint in prompt_api/app/routers/prompts.py */
@Injectable({ providedIn: 'root' })
export class PromptApiService {
  private readonly http = inject(HttpClient);

  list(filters: PromptFilters): Observable<Prompt[]> {
    let params = new HttpParams();
    if (filters.category) params = params.set('category', filters.category);
    if (filters.favorite !== undefined) params = params.set('favorite', filters.favorite);
    if (filters.tag) params = params.set('tag', filters.tag);
    return this.http.get<Prompt[]>(API, { params });
  }

  get(id: number): Observable<Prompt> {
    return this.http.get<Prompt>(`${API}/${id}`);
  }

  create(data: PromptCreate): Observable<Prompt> {
    return this.http.post<Prompt>(API, data);
  }

  update(id: number, data: PromptUpdate): Observable<Prompt> {
    return this.http.patch<Prompt>(`${API}/${id}`, data);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${API}/${id}`);
  }
}
