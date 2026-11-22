import { DatePipe } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

import { PromptApiService } from './core/prompt-api.service';
import { Prompt, PromptCreate, PromptFilters } from './core/prompt.model';

type FavoriteFilter = 'all' | 'yes' | 'no';

@Component({
  selector: 'app-root',
  imports: [ReactiveFormsModule, DatePipe],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App implements OnInit {
  private readonly api = inject(PromptApiService);
  private readonly fb = inject(FormBuilder);

  protected readonly prompts = signal<Prompt[]>([]);
  protected readonly loading = signal(false);
  protected readonly listError = signal<string | null>(null);

  // filters -> query params of GET /prompts
  protected readonly category = signal('');
  protected readonly favorite = signal<FavoriteFilter>('all');
  protected readonly tag = signal('');
  protected readonly hasFilters = computed(
    () => !!this.category() || this.favorite() !== 'all' || !!this.tag(),
  );

  // editor: null = closed, 'new' = POST, number = PATCH that id
  protected readonly editing = signal<'new' | number | null>(null);
  protected readonly saving = signal(false);
  protected readonly formErrors = signal<string[]>([]);

  protected readonly form = this.fb.nonNullable.group({
    title: ['', [Validators.required, Validators.maxLength(200)]],
    category: ['', [Validators.required, Validators.maxLength(50)]],
    body: ['', Validators.required],
    tags: [''],
    is_favorite: [false],
  });

  ngOnInit(): void {
    this.load();
  }

  protected load(): void {
    const filters: PromptFilters = {
      category: this.category().trim() || undefined,
      favorite: this.favorite() === 'all' ? undefined : this.favorite() === 'yes',
      tag: this.tag().trim() || undefined,
    };
    this.loading.set(true);
    this.listError.set(null);
    this.api.list(filters).subscribe({
      next: (list) => {
        this.prompts.set(list);
        this.loading.set(false);
      },
      error: (err: HttpErrorResponse) => {
        this.listError.set(this.describe(err).join(' '));
        this.loading.set(false);
      },
    });
  }

  protected setCategory(value: string): void {
    this.category.set(value);
    this.load();
  }

  protected setFavorite(value: string): void {
    this.favorite.set(value as FavoriteFilter);
    this.load();
  }

  protected setTag(value: string): void {
    this.tag.set(value);
    this.load();
  }

  protected resetFilters(): void {
    this.category.set('');
    this.favorite.set('all');
    this.tag.set('');
    this.load();
  }

  protected openNew(): void {
    this.form.reset();
    this.formErrors.set([]);
    this.editing.set('new');
  }

  protected openEdit(prompt: Prompt): void {
    this.form.setValue({
      title: prompt.title,
      category: prompt.category,
      body: prompt.body,
      tags: prompt.tags.map((t) => t.name).join(', '),
      is_favorite: prompt.is_favorite,
    });
    this.formErrors.set([]);
    this.editing.set(prompt.id);
  }

  protected closeEditor(): void {
    this.editing.set(null);
  }

  protected save(): void {
    const target = this.editing();
    if (target === null) return;

    const value = this.form.getRawValue();
    const data: PromptCreate = {
      ...value,
      tags: value.tags
        .split(',')
        .map((t) => t.trim())
        .filter(Boolean),
    };

    this.saving.set(true);
    const request = target === 'new' ? this.api.create(data) : this.api.update(target, data);
    request.subscribe({
      next: () => {
        this.saving.set(false);
        this.editing.set(null);
        this.load();
      },
      error: (err: HttpErrorResponse) => {
        this.saving.set(false);
        this.formErrors.set(this.describe(err));
      },
    });
  }

  protected toggleFavorite(prompt: Prompt): void {
    // PATCH with a single field: exactly what exclude_unset is for
    this.api.update(prompt.id, { is_favorite: !prompt.is_favorite }).subscribe({
      next: () => this.load(),
      error: (err: HttpErrorResponse) => this.listError.set(this.describe(err).join(' ')),
    });
  }

  protected remove(prompt: Prompt): void {
    this.api.delete(prompt.id).subscribe({
      next: () => this.load(),
      error: (err: HttpErrorResponse) => this.listError.set(this.describe(err).join(' ')),
    });
  }

  /** Turns FastAPI errors into readable lines (422 detail is a list, 404 detail is a string) */
  private describe(err: HttpErrorResponse): string[] {
    if (err.status === 0 || (err.status >= 500 && !err.error?.detail)) {
      return ['API is not reachable. Start it in prompt_api: uv run fastapi dev app/main.py'];
    }
    const detail = err.error?.detail;
    if (Array.isArray(detail)) {
      return detail.map((d: { loc: (string | number)[]; msg: string }) => {
        const field = d.loc.filter((part) => part !== 'body').join('.');
        return field ? `${field}: ${d.msg}` : d.msg;
      });
    }
    if (typeof detail === 'string') return [`${err.status}: ${detail}`];
    return [`${err.status} ${err.statusText}`];
  }
}
