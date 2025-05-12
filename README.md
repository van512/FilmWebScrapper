# 🎬 Film Metadata Scraper

**Author**: [Evanne Smith]  
**Date**: [May 2025]  
**Repository**: [[https://github.com/van512/FilmWebScrapper](https://github.com/van512/FilmWebScrapper)]

---

## 🧠 Project Overview

This project collects structured metadata about films produced in the United Kingdom (and optionally other countries) over the past decade, using **The Movie Database (TMDb) API**.  

It also extracts information about key creative personnel — including **directors**, **producers**, and **main cast members** — and analyzes their **career histories** (years active, previous films, roles).

---

## 🚀 How to Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/van512/FilmWebScrapper.git
   cd FilmWebScrapper
   ```

2. **Set up environment**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your TMDb API Key**:
   - Sign up at [TMDb API](https://www.themoviedb.org/documentation/api)
   - Export it to your environment:
     ```bash
     export TMDB_API_KEY="your_api_key_here"
     ```

4. **Run the scraper**:
   ```bash
   python src/simple_scrape.py
   ```

## 📈 Example Visualizations

very minimalistic still

```bash
streamlit run streamlit_app.py
```

---

## 📜 License

https://www.themoviedb.org/about/logos-attribution





