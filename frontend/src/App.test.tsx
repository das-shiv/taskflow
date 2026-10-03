import '@testing-library/jest-dom/vitest';
import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import App from './App';

describe('App', () => {
  it('renders the TaskFlow heading', () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, json: async () => [] }));
    render(<App />);
    expect(screen.getByRole('heading', { name: 'TaskFlow' })).toBeInTheDocument();
  });
});

