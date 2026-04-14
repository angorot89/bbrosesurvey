import json, os, io, qrcode, math
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from .models import Employee


def index(request):
    return render(request, 'questionnaire/index.html')


def profile(request, employee_id):
    emp = get_object_or_404(Employee, employee_id=employee_id)
    photo_url = emp.photo.url if emp.photo else None
    id_card_url = emp.id_card.url if emp.id_card else None
    qr_code_url = emp.qr_code.url if emp.qr_code else None
    return render(request, 'questionnaire/profile.html', {
        'emp': emp,
        'photo_url': photo_url,
        'id_card_url': id_card_url,
        'qr_code_url': qr_code_url,
    })


@csrf_exempt
def submit(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.POST.get('data', '{}'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    emp = Employee()
    emp.language = data.get('language', 'en')
    emp.full_name = data.get('full_name', '')
    emp.english_name = data.get('english_name', '')
    emp.phone = data.get('phone', '')
    emp.email = data.get('email', '')
    emp.role = data.get('role', '')
    emp.id_type = data.get('id_type', 'id')
    emp.id_number = data.get('id_number', '')
    emp.consent_given = data.get('consent', False)

    emp.role_responsibilities = data.get('role_responsibilities', {})
    emp.workflow_efficiency = data.get('workflow_efficiency', {})
    emp.pain_points = data.get('pain_points', {})
    emp.communication = data.get('communication', {})
    emp.tools_technology = data.get('tools_technology', {})
    emp.ideas_suggestions = data.get('ideas_suggestions', {})

    if 'photo' in request.FILES:
        emp.photo = request.FILES['photo']
    else:
        return JsonResponse({'error': 'Photo required'}, status=400)

    emp.save()

    profile_url = request.build_absolute_uri(f'/profile/{emp.employee_id}/')

    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(profile_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#06b6d4", back_color="white").convert('RGB')
    qr_buf = io.BytesIO()
    qr_img.save(qr_buf, format='PNG')
    emp.qr_code.save(f'qr_{emp.employee_id}.png', ContentFile(qr_buf.getvalue()), save=False)

    card = generate_id_card(emp, qr_img)
    card_buf = io.BytesIO()
    card.save(card_buf, format='PNG')
    emp.id_card.save(f'idcard_{emp.employee_id}.png', ContentFile(card_buf.getvalue()), save=False)

    emp.save()

    return JsonResponse({
        'success': True,
        'employee_id': emp.employee_id,
        'id_card_url': emp.id_card.url,
        'qr_code_url': emp.qr_code.url,
        'full_name': emp.full_name,
        'role': emp.role,
        'photo_url': emp.photo.url if emp.photo else None,
        'profile_url': profile_url,
    })


@csrf_exempt
def update_employee(request, employee_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    emp = get_object_or_404(Employee, employee_id=employee_id)

    try:
        data = json.loads(request.POST.get('data', '{}'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if 'full_name' in data and data['full_name']:
        emp.full_name = data['full_name']
    if 'role' in data:
        emp.role = data['role']
    if 'id_type' in data:
        emp.id_type = data['id_type']
    if 'id_number' in data:
        emp.id_number = data['id_number']
    if 'photo' in request.FILES:
        emp.photo = request.FILES['photo']

    emp.save()

    profile_url = request.build_absolute_uri(f'/profile/{emp.employee_id}/')

    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(profile_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#06b6d4", back_color="white").convert('RGB')
    qr_buf = io.BytesIO()
    qr_img.save(qr_buf, format='PNG')
    emp.qr_code.save(f'qr_{emp.employee_id}.png', ContentFile(qr_buf.getvalue()), save=False)

    card = generate_id_card(emp, qr_img)
    card_buf = io.BytesIO()
    card.save(card_buf, format='PNG')
    emp.id_card.save(f'idcard_{emp.employee_id}.png', ContentFile(card_buf.getvalue()), save=False)

    emp.save()

    return JsonResponse({
        'success': True,
        'id_card_url': emp.id_card.url,
        'qr_code_url': emp.qr_code.url,
        'full_name': emp.full_name,
        'role': emp.role,
        'photo_url': emp.photo.url if emp.photo else None,
    })


@csrf_exempt
def regenerate_badge(request, employee_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    emp = get_object_or_404(Employee, employee_id=employee_id)

    profile_url = request.build_absolute_uri(f'/profile/{emp.employee_id}/')

    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(profile_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#06b6d4", back_color="white").convert('RGB')
    qr_buf = io.BytesIO()
    qr_img.save(qr_buf, format='PNG')
    emp.qr_code.save(f'qr_{emp.employee_id}.png', ContentFile(qr_buf.getvalue()), save=False)

    card = generate_id_card(emp, qr_img)
    card_buf = io.BytesIO()
    card.save(card_buf, format='PNG')
    emp.id_card.save(f'idcard_{emp.employee_id}.png', ContentFile(card_buf.getvalue()), save=False)

    emp.save()

    return JsonResponse({
        'success': True,
        'id_card_url': emp.id_card.url,
        'qr_code_url': emp.qr_code.url,
    })


# ─────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────

def _lerp_color(c1, c2, t):
    """Linear-interpolate between two (R,G,B) tuples."""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def _draw_rounded_rect_rgba(img_rgba, xy, radius, fill_rgba):
    """Draw a rounded rectangle on an RGBA image."""
    x0, y0, x1, y1 = xy
    r = radius
    overlay = Image.new('RGBA', img_rgba.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill_rgba)
    img_rgba.alpha_composite(overlay)


def _draw_glow_circle(img_rgba, cx, cy, radius, color_rgb, alpha_peak=120, steps=12):
    """Simulate a radial glow by drawing concentric translucent circles."""
    for i in range(steps, 0, -1):
        t = i / steps
        r = int(radius * t)
        a = int(alpha_peak * (1 - t) ** 1.5)
        overlay = Image.new('RGBA', img_rgba.size, (0, 0, 0, 0))
        ImageDraw.Draw(overlay).ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            fill=(*color_rgb, a)
        )
        img_rgba.alpha_composite(overlay)


def _draw_rainbow_bar(img_rgba, y, height=8):
    """Draw a horizontal rainbow gradient bar."""
    W = img_rgba.width
    stops = [
        (244, 63,  94),   # rose
        (249, 115, 22),   # orange
        (234, 179,  8),   # yellow
        (34,  197, 94),   # green
        (6,   182, 212),  # cyan
        (59,  130, 246),  # blue
        (139, 92,  246),  # violet
        (236, 72,  153),  # pink
        (244, 63,  94),   # rose again (seamless)
    ]
    n = len(stops) - 1
    overlay = Image.new('RGBA', img_rgba.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for x in range(W):
        t_global = x / W * n
        seg = int(t_global)
        seg = min(seg, n - 1)
        t_local = t_global - seg
        c = _lerp_color(stops[seg], stops[seg + 1], t_local)
        draw.line([(x, y), (x, y + height - 1)], fill=(*c, 255))
    img_rgba.alpha_composite(overlay)


def _draw_circle_photo(card_rgba, photo_path, cx, cy, size):
    """Paste a circular photo (or placeholder) with a neon glow ring."""
    radius = size // 2

    # Glow rings (outer to inner)
    _draw_glow_circle(card_rgba, cx, cy, radius + 22, (6, 182, 212), alpha_peak=80, steps=10)

    # Cyan ring 1
    ring1 = Image.new('RGBA', card_rgba.size, (0, 0, 0, 0))
    ImageDraw.Draw(ring1).ellipse(
        [cx - radius - 6, cy - radius - 6, cx + radius + 6, cy + radius + 6],
        fill=(6, 182, 212, 200)
    )
    card_rgba.alpha_composite(ring1)

    # Dark separator ring
    ring2 = Image.new('RGBA', card_rgba.size, (0, 0, 0, 0))
    ImageDraw.Draw(ring2).ellipse(
        [cx - radius - 3, cy - radius - 3, cx + radius + 3, cy + radius + 3],
        fill=(6, 18, 42, 240)
    )
    card_rgba.alpha_composite(ring2)

    # Circle mask for photo
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)

    if photo_path and os.path.exists(photo_path):
        try:
            photo = Image.open(photo_path).convert('RGB')
            # Crop to square first
            w, h = photo.size
            m = min(w, h)
            photo = photo.crop(((w - m) // 2, (h - m) // 2, (w + m) // 2, (h + m) // 2))
            photo = photo.resize((size, size), Image.LANCZOS)
            photo_rgba = photo.convert('RGBA')
            photo_rgba.putalpha(mask)
            card_rgba.alpha_composite(photo_rgba, (cx - radius, cy - radius))
            return
        except Exception:
            pass

    # Placeholder gradient circle
    grad = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    grad_draw = ImageDraw.Draw(grad)
    for i in range(size):
        t = i / size
        c = _lerp_color((14, 79, 110), (76, 29, 149), t)
        grad_draw.line([(0, i), (size, i)], fill=(*c, 255))
    grad.putalpha(mask)
    card_rgba.alpha_composite(grad, (cx - radius, cy - radius))

    # "?" icon in placeholder
    try:
        fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size // 3)
    except Exception:
        fnt = ImageFont.load_default()
    tmp = ImageDraw.Draw(card_rgba)
    bbox = tmp.textbbox((0, 0), "?", font=fnt)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tmp.text((cx - tw // 2, cy - th // 2), "?", fill=(103, 232, 249, 200), font=fnt)


def generate_id_card(emp, qr_img):
    W, H = 1080, 620
    CARD_R = (6, 16, 42)      # dark navy
    CARD_G = (19, 7, 34)      # deep purple-black
    CARD_B = (7, 28, 46)      # dark teal-black

    # ── Background gradient (dark navy → deep purple → dark teal) ──
    card = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(card)
    for y in range(H):
        t = y / H
        if t < 0.45:
            c = _lerp_color(CARD_R, CARD_G, t / 0.45)
        else:
            c = _lerp_color(CARD_G, CARD_B, (t - 0.45) / 0.55)
        draw.line([(0, y), (W, y)], fill=(*c, 255))

    # ── Ambient glow blobs ──
    _draw_glow_circle(card, -60, -60, 280, (6, 182, 212), alpha_peak=55, steps=14)   # top-left cyan
    _draw_glow_circle(card, W + 40, H + 40, 260, (139, 92, 246), alpha_peak=55, steps=14)  # bottom-right violet
    _draw_glow_circle(card, 320, H - 20, 180, (244, 63, 94), alpha_peak=40, steps=10)      # bottom-mid rose

    # Subtle dot-grid pattern
    for gx in range(0, W, 28):
        for gy in range(0, H, 28):
            overlay = Image.new('RGBA', card.size, (0, 0, 0, 0))
            ImageDraw.Draw(overlay).ellipse([gx, gy, gx + 1, gy + 1], fill=(255, 255, 255, 12))
            card.alpha_composite(overlay)

    # ── Rainbow shimmer bar ──
    _draw_rainbow_bar(card, y=0, height=8)

    # ── Thin border on card edges ──
    border_overlay = Image.new('RGBA', card.size, (0, 0, 0, 0))
    ImageDraw.Draw(border_overlay).rectangle([0, 0, W - 1, H - 1], outline=(255, 255, 255, 18), width=2)
    card.alpha_composite(border_overlay)

    # ─── Fonts ───
    def load_font(path, size, fallback_size=None):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            return ImageFont.load_default()

    BOLD   = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    REG    = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    MONO   = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

    f_company   = load_font(BOLD, 34)
    f_sub       = load_font(REG,  15)
    f_name      = load_font(BOLD, 32)
    f_role_sm   = load_font(BOLD, 15)
    f_label     = load_font(REG,  13)
    f_value     = load_font(REG,  17)
    f_id        = load_font(MONO, 17)
    f_footer    = load_font(REG,  12)
    f_official  = load_font(BOLD, 11)
    f_doc_value = load_font(BOLD, 18)

    draw = ImageDraw.Draw(card)

    # ── Logo + Brand row ──
    logo_x, logo_y = 34, 18
    logo_path = os.path.join(settings.BASE_DIR, 'questionnaire', 'static', 'questionnaire', 'img', 'logo.png')
    if os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert('RGBA')
            logo.thumbnail((82, 82), Image.LANCZOS)
            # Convert logo to white
            r, g, b, a = logo.split()
            white_logo = Image.merge('RGBA', (
                Image.new('L', logo.size, 255),
                Image.new('L', logo.size, 255),
                Image.new('L', logo.size, 255),
                a
            ))
            card.alpha_composite(white_logo, (logo_x, logo_y))
        except Exception:
            pass

    draw.text((logo_x + 94, logo_y + 8),  "BBROSE", fill=(255, 255, 255, 240), font=f_company)
    draw.text((logo_x + 96, logo_y + 46), "EMPLOYEE IDENTITY CARD", fill=(103, 232, 249, 150), font=f_sub)

    # "OFFICIAL" holotag top-right
    tag_text = "OFFICIAL"
    tag_bbox = draw.textbbox((0, 0), tag_text, font=f_official)
    tag_w, tag_h = tag_bbox[2] - tag_bbox[0], tag_bbox[3] - tag_bbox[1]
    tag_x, tag_y = W - tag_w - 48, logo_y + 20
    _draw_rounded_rect_rgba(card, [tag_x - 10, tag_y - 5, tag_x + tag_w + 10, tag_y + tag_h + 5],
                            radius=4, fill_rgba=(6, 182, 212, 40))
    border_tag = Image.new('RGBA', card.size, (0, 0, 0, 0))
    ImageDraw.Draw(border_tag).rounded_rectangle(
        [tag_x - 10, tag_y - 5, tag_x + tag_w + 10, tag_y + tag_h + 5],
        radius=4, outline=(6, 182, 212, 120), width=1)
    card.alpha_composite(border_tag)
    draw = ImageDraw.Draw(card)
    draw.text((tag_x, tag_y), tag_text, fill=(103, 232, 249, 200), font=f_official)

    # ── Vertical separator line ──
    sep_x = 320
    sep_line = Image.new('RGBA', card.size, (0, 0, 0, 0))
    ImageDraw.Draw(sep_line).line([(sep_x, 90), (sep_x, H - 55)], fill=(255, 255, 255, 25), width=1)
    card.alpha_composite(sep_line)

    # ── Photo ──
    photo_cx, photo_cy = 170, 300
    photo_size = 220
    photo_path = emp.photo.path if emp.photo else None
    _draw_circle_photo(card, photo_path, photo_cx, photo_cy, photo_size)

    draw = ImageDraw.Draw(card)

    # ── QR Code (below photo) ──
    qr_size = 126
    qr_x = photo_cx - qr_size // 2
    qr_y = photo_cy + photo_size // 2 + 22

    # White card behind QR
    qr_card = Image.new('RGBA', card.size, (0, 0, 0, 0))
    ImageDraw.Draw(qr_card).rounded_rectangle(
        [qr_x - 8, qr_y - 8, qr_x + qr_size + 8, qr_y + qr_size + 8],
        radius=10, fill=(255, 255, 255, 255)
    )
    card.alpha_composite(qr_card)
    qr_resized = qr_img.resize((qr_size, qr_size), Image.LANCZOS).convert('RGBA')
    card.alpha_composite(qr_resized, (qr_x, qr_y))

    draw = ImageDraw.Draw(card)
    draw.text((qr_x + qr_size // 2 - 28, qr_y + qr_size + 10), "Scan Profile",
              fill=(103, 232, 249, 120), font=f_footer)

    # ── Info section ──
    info_x = sep_x + 42
    info_y = 112

    # Full name
    name = emp.full_name or "—"
    draw.text((info_x, info_y), name, fill=(255, 255, 255, 240), font=f_name)
    name_bbox = draw.textbbox((info_x, info_y), name, font=f_name)
    name_h = name_bbox[3] - name_bbox[1]

    # Role pill
    role_text = emp.role or "Team Member"
    role_y = info_y + name_h + 12
    role_bbox = draw.textbbox((0, 0), role_text, font=f_role_sm)
    role_w = role_bbox[2] - role_bbox[0]
    pill_pad_x, pill_pad_y = 16, 6
    pill_x0, pill_y0 = info_x, role_y
    pill_x1, pill_y1 = info_x + role_w + pill_pad_x * 2, role_y + (role_bbox[3] - role_bbox[1]) + pill_pad_y * 2
    # Gradient pill background
    pill_img = Image.new('RGBA', card.size, (0, 0, 0, 0))
    pill_draw = ImageDraw.Draw(pill_img)
    for px in range(pill_x0, pill_x1):
        t = (px - pill_x0) / max(pill_x1 - pill_x0, 1)
        c = _lerp_color((6, 182, 212), (139, 92, 246), t)
        pill_draw.line([(px, pill_y0), (px, pill_y1)], fill=(*c, 60))
    card.alpha_composite(pill_img)
    pill_border = Image.new('RGBA', card.size, (0, 0, 0, 0))
    ImageDraw.Draw(pill_border).rounded_rectangle(
        [pill_x0, pill_y0, pill_x1, pill_y1], radius=20,
        outline=(6, 182, 212, 150), width=1
    )
    card.alpha_composite(pill_border)
    draw = ImageDraw.Draw(card)
    draw.text((pill_x0 + pill_pad_x, pill_y0 + pill_pad_y), role_text,
              fill=(103, 232, 249, 230), font=f_role_sm)

    # Divider
    div_y = pill_y1 + 20
    div_line = Image.new('RGBA', card.size, (0, 0, 0, 0))
    ImageDraw.Draw(div_line).line([(info_x, div_y), (W - 52, div_y)], fill=(255, 255, 255, 30), width=1)
    card.alpha_composite(div_line)
    draw = ImageDraw.Draw(card)

    # Fields
    def draw_field(y, label, value):
        draw.text((info_x, y), label.upper(), fill=(255, 255, 255, 80), font=f_label)
        draw.text((info_x, y + 18), value or "—", fill=(255, 255, 255, 195), font=f_value)
        return y + 58

    fy = div_y + 16
    if emp.email:
        fy = draw_field(fy, "Email", emp.email)
    if emp.phone:
        fy = draw_field(fy, "Phone", emp.phone)

    doc_label = "Passport Number" if (emp.id_type or '').lower() == 'passport' else "ID Number"
    doc_type = "Passport" if (emp.id_type or '').lower() == 'passport' else "National ID"
    doc_box_y = fy + 4
    doc_box_h = 94
    doc_box = Image.new('RGBA', card.size, (0, 0, 0, 0))
    ImageDraw.Draw(doc_box).rounded_rectangle(
        [info_x, doc_box_y, W - 56, doc_box_y + doc_box_h],
        radius=18, fill=(255, 255, 255, 18), outline=(255, 255, 255, 30), width=1
    )
    card.alpha_composite(doc_box)
    draw = ImageDraw.Draw(card)
    draw.text((info_x + 18, doc_box_y + 16), doc_type.upper(), fill=(103, 232, 249, 190), font=f_label)
    draw.text((info_x + 18, doc_box_y + 36), emp.id_number or "—", fill=(255, 255, 255, 235), font=f_doc_value)
    draw.text((info_x + 18, doc_box_y + 62), doc_label, fill=(255, 255, 255, 90), font=f_label)

    # Employee ID badge
    id_text = emp.employee_id
    id_y = doc_box_y + doc_box_h + 18
    id_bbox = draw.textbbox((0, 0), id_text, font=f_id)
    id_w = id_bbox[2] - id_bbox[0]
    ib_pad = 14
    ib_x0, ib_y0 = info_x, id_y
    ib_x1, ib_y1 = info_x + id_w + ib_pad * 2, id_y + (id_bbox[3] - id_bbox[1]) + ib_pad

    # ID badge glow
    _draw_glow_circle(card, (ib_x0 + ib_x1) // 2, (ib_y0 + ib_y1) // 2,
                      max(id_w, 60), (6, 182, 212), alpha_peak=35, steps=6)
    id_bg = Image.new('RGBA', card.size, (0, 0, 0, 0))
    ImageDraw.Draw(id_bg).rounded_rectangle(
        [ib_x0, ib_y0, ib_x1, ib_y1], radius=8, fill=(6, 182, 212, 28)
    )
    card.alpha_composite(id_bg)
    id_border = Image.new('RGBA', card.size, (0, 0, 0, 0))
    ImageDraw.Draw(id_border).rounded_rectangle(
        [ib_x0, ib_y0, ib_x1, ib_y1], radius=8, outline=(6, 182, 212, 160), width=1
    )
    card.alpha_composite(id_border)
    draw = ImageDraw.Draw(card)
    draw.text((ib_x0 + ib_pad, ib_y0 + ib_pad // 2), id_text,
              fill=(6, 182, 212, 240), font=f_id)

    # ── Footer bar ──
    footer_h = 46
    footer_y = H - footer_h
    footer_bg = Image.new('RGBA', card.size, (0, 0, 0, 0))
    footer_draw = ImageDraw.Draw(footer_bg)
    for x in range(W):
        t = x / W
        c1 = _lerp_color((6, 182, 212), (139, 92, 246), t)
        c2 = _lerp_color((139, 92, 246), (244, 63, 94), t)
        c = _lerp_color(c1, c2, t)
        footer_draw.line([(x, footer_y), (x, H)], fill=(*c, 22))
    card.alpha_composite(footer_bg)
    border_footer = Image.new('RGBA', card.size, (0, 0, 0, 0))
    ImageDraw.Draw(border_footer).line([(0, footer_y), (W, footer_y)], fill=(255, 255, 255, 22), width=1)
    card.alpha_composite(border_footer)
    draw = ImageDraw.Draw(card)
    draw.text((36, footer_y + 14), "BBrose Internal  •  Confidential  •  Not for external distribution",
              fill=(255, 255, 255, 65), font=f_footer)

    return card.convert('RGB')
