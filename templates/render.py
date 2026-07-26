#!/usr/bin/env python3
"""Render scene.html to an mp4 by seeking a deterministic timeline frame by frame.

    python render.py                 # full render -> promo.mp4
    python render.py --contact       # 24-frame contact sheet only (fast preview)
    python render.py --at 6.2 8.0    # single frames at given seconds -> preview_*.png
"""
import argparse, http.server, os, shutil, socketserver, subprocess, sys, threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
FPS = 30
W, H = 1080, 1920


def serve(directory):
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=str(directory), **k)
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--contact", action="store_true")
    ap.add_argument("--at", nargs="*", type=float)
    ap.add_argument("--out", default=str(HERE / "promo.mp4"))
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    httpd, port = serve(HERE)
    frames = HERE / ".frames"

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--force-color-profile=srgb",
                                          "--disable-lcd-text",
                                          "--hide-scrollbars"])
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        page.goto(f"http://127.0.0.1:{port}/scene.html")
        page.wait_for_function("window.__ready === true", timeout=30000)
        dur = page.evaluate("DUR")

        if args.at:
            for t in args.at:
                page.evaluate("t => window.seek(t)", t)
                page.screenshot(path=str(HERE / f"preview_{t:.2f}.png"))
            print("wrote previews")
            browser.close(); httpd.shutdown(); return

        if args.contact:
            sheetdir = HERE / ".sheet"
            shutil.rmtree(sheetdir, ignore_errors=True); sheetdir.mkdir()
            n = 24
            for i in range(n):
                t = dur * (i + 0.5) / n
                page.evaluate("t => window.seek(t)", t)
                page.screenshot(path=str(sheetdir / f"{i:03d}.png"))
            browser.close(); httpd.shutdown()
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "1",
                            "-i", str(sheetdir / "%03d.png"),
                            "-vf", "scale=270:480,tile=8x3", "-frames:v", "1",
                            str(HERE / "contact.png")], check=True)
            print("wrote contact.png")
            return

        shutil.rmtree(frames, ignore_errors=True); frames.mkdir()
        total = int(round(dur * FPS))
        for i in range(total):
            page.evaluate("t => window.seek(t)", i / FPS)
            page.screenshot(path=str(frames / f"{i:05d}.png"))
            if i % 60 == 0:
                print(f"  {i}/{total}", flush=True)
        browser.close(); httpd.shutdown()

    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-framerate", str(FPS), "-i", str(frames / "%05d.png"),
        "-c:v", "libx264", "-preset", "slow", "-crf", "17",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-vf", "format=yuv420p", args.out,
    ], check=True)
    shutil.rmtree(frames, ignore_errors=True)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
