<<<<<<< HEAD

## Getting Started

First, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.
=======
# Sentinal-x
<<<<<<< HEAD
>>>>>>> 3b289aa6266cbf1e5b77e0eef39598244a66316b
=======
# Sentinel-X Data Integration
>>>>>>> data-integration

## Overview

This directory contains the data-integration layer for Sentinel-X.

The purpose of this layer is to collect sample event data in a consistent raw format, normalize the data using Python scripts, and provide structured output that can later be consumed by the backend and Firebase services.

## Data Pipeline

```text
Raw JSON Data
      ↓
Normalization Scripts
      ↓
Normalized JSON Data
      ↓
Backend / Firebase
