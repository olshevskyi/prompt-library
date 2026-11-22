import { HttpErrorResponse, HttpInterceptorFn, HttpResponse } from '@angular/common/http';
import { Injectable, inject, signal } from '@angular/core';
import { tap } from 'rxjs';

export interface ApiLogEntry {
  id: number;
  method: string;
  url: string;
  status: number;
  ms: number;
  requestBody: unknown;
  responseBody: unknown;
}

/** Keeps the last requests so the UI can show what the FastAPI backend did */
@Injectable({ providedIn: 'root' })
export class ApiLog {
  private nextId = 1;
  readonly entries = signal<ApiLogEntry[]>([]);

  add(entry: Omit<ApiLogEntry, 'id'>): void {
    this.entries.update((list) => [{ ...entry, id: this.nextId++ }, ...list].slice(0, 30));
  }

  clear(): void {
    this.entries.set([]);
  }
}

export const apiLogInterceptor: HttpInterceptorFn = (req, next) => {
  const log = inject(ApiLog);
  const started = performance.now();
  const record = (status: number, responseBody: unknown) =>
    log.add({
      method: req.method,
      url: req.urlWithParams.replace(/^\/api/, ''),
      status,
      ms: Math.round(performance.now() - started),
      requestBody: req.body,
      responseBody,
    });

  return next(req).pipe(
    tap({
      next: (event) => {
        if (event instanceof HttpResponse) record(event.status, event.body);
      },
      error: (err: HttpErrorResponse) => record(err.status, err.error),
    }),
  );
};
