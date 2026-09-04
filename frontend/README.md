# Meridian Frontend

A modern Next.js App Router application built for Meridian Commercial Intelligence.

## Structure
- `src/app` — App Router pages (`/`, `/opportunities`, `/campaigns`, `/checkout`, `/customers`, `/products`, `/experiments`, `/activity`, `/settings`, `/transactions`)
- `src/components` — Reusable UI components
  - `src/components/ui` — Base design system pieces (`Badge`, `Button`, `Card`, `Sidebar`, `StatNumber`)
  - `src/components/dashboard` — Feature panels (`AlertsPanel`, `ChatPanel`)
- `src/hooks` — Custom React hooks
- `src/lib` — Utilities and API client helpers (`api.ts`)
- `src/types` — Shared TypeScript types and interfaces (`index.ts`)
- `src/context` — React Context providers
- `src/assets` — Static image assets and icons

## Getting Started

```bash
npm install
npm run dev
```

Runs the application at [http://localhost:3000](http://localhost:3000).

## Build Verification

```bash
npm run build
```

Performs full TypeScript compilation and Next.js App Router production build.
