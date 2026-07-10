# HerSakhi - AI Career Companion

HerSakhi is a comprehensive, AI-driven career companion for women, integrating career roadmap generation, resume analysis, skill gap tracking, and AI mentorship.

## Features
- **Premium UI/UX:** Built with Three.js, GSAP, and a custom glassmorphism design system.
- **Centralized AI:** Integrated OpenRouter support with fallback mechanisms.
- **Django Monolith:** Robust backend serving customized templates and robust REST APIs.

## Environment Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables:**
   Copy `.env.example` to `.env` and fill in your actual credentials.
   ```bash
   cp .env.example .env
   ```
   *Note: The application is environment-driven. Ensure `DATABASE_URL` and `OPENROUTER_API_KEY` are set.*

3. **Database Migration:**
   Apply database migrations.
   ```bash
   python manage.py migrate
   ```

4. **Running the Development Server:**
   Start the Django development server.
   ```bash
   python manage.py runserver
   ```
   The site will be available at `http://localhost:8000/`.

## Architecture Note
The project uses a monolithic Django architecture. Frontend assets (HTML, CSS, JS, Three.js models) are stored natively within the `templates` and `static` directories and served by Django, completely eliminating the need for a separate node frontend. The AI services are heavily modularized in the `ai/` package, and all AI features communicate through Django REST Framework endpoints.
