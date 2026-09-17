from pathlib import Path
import json
import html

people = [
    ('lucia', 'Lucía Fernández', 'Docente de preescolar', 'Una forma sencilla de hablar de convivencia', 'Me encanta que las escenas partan de situaciones cotidianas. Son un punto de partida muy práctico para conversar sobre compartir, respetar turnos y cuidar a los demás. ¡Una propuesta bonita para aprender jugando!', '50% 35%'),
    ('carmen', 'Carmen Rodríguez', 'Docente de primaria', 'Descargar, imprimir y empezar', 'Lo que más me gusta es tener las ilustraciones listas para imprimir. El formato de juego permite preparar una actividad sobre normas de convivencia sin tener que diseñar todo desde cero. ¡Muy práctico para la rutina del aula!', '50% 30%'),
    ('valentina', 'Valentina Morales', 'Madre de familia', 'Pequeñas escenas, grandes conversaciones', 'Me parece una idea preciosa para compartir en casa. Mirar una escena y preguntar «¿se puede o no se puede?» invita a escuchar lo que piensan los niños y a conversar sobre cómo nuestras acciones afectan a los demás.', '45% 35%'),
    ('mariana', 'Mariana Castillo', 'Educadora infantil', 'Más ideas para seguir aprendiendo', 'Me gusta que, además del juego de convivencia, incluya materiales de letras, sílabas y memoria. Los seis bonos ofrecen variedad para proponer otras actividades y seguir aprendiendo de una manera entretenida.', '55% 43%'),
]
cards = []
for slug, name, role, title, quote, position in people:
    rating = '4,5' if slug == 'mariana' else '5'
    stars = ''.join('<span class="testimonial__star' + (' testimonial__star--half' if rating == '4,5' and i == 4 else '') + '">★</span>' for i in range(5))
    rating_html = f'<div class="testimonial__rating" role="img" aria-label="{rating} de 5 estrellas"><span class="testimonial__stars" aria-hidden="true">{stars}</span><span class="testimonial__score" aria-hidden="true">{rating}/5</span></div>'
    cards.append(f'<figure class="testimonial">{rating_html}<blockquote><strong>{html.escape(title)}</strong>{html.escape(quote)}</blockquote><figcaption><img src="assets/testimonials/{slug}.jpg" alt="Foto de {name}" width="68" height="68" loading="lazy" decoding="async" style="object-position:{position}"/><div><strong>{name}</strong><span class="testimonial__role">{role}</span></div></figcaption></figure>')
content = '<div class="testimonials__inner"><header class="testimonials__header"><span class="testimonials__eyebrow">Para el aula y el hogar</span><h2 id="testimonios-title">Convivir también se aprende <span>jugando</span></h2><p class="testimonials__intro">Cuatro miradas sobre cómo aprovechar ¿Se Puede o No Se Puede? en el día a día.</p></header><div class="testimonials__grid">' + ''.join(cards) + '</div></div>'
Path('assets/testimonials.js').write_text('// Shared with static HTML to preserve React hydration.\nexport const testimonialContent = ' + json.dumps(content, ensure_ascii=False) + ';\n', encoding='utf-8')
section = '<section id="testimonios" class="testimonials" aria-labelledby="testimonios-title">' + content + '</section>'
p = Path('index.html')
s = p.read_text(encoding='utf-8')
if '<section id="testimonios"' in s:
    start = s.index('<section id="testimonios"')
    end = s.index('</section>', start) + len('</section>')
    s = s[:start] + section + s[end:]
else:
    start = s.rfind('<section ', 0, s.index('Para quién es'))
    assert start > 0
    s = s[:start] + section + s[start:]
if 'href="assets/testimonials.css"' not in s:
    s = s.replace('</head>', '<link rel="stylesheet" href="assets/testimonials.css"/></head>')
p.write_text(s, encoding='utf-8')
p = Path('assets/index-Dp6CYv2J.js')
s = p.read_text(encoding='utf-8')
if 'import {testimonialContent}' not in s:
    s = 'import {testimonialContent} from "./testimonials.js";\n' + s
    old = 'o.jsx(er,{}),o.jsx(tr,{})'
    assert s.count(old) == 1
    s = s.replace(old, 'o.jsx(er,{}),o.jsx("section",{id:"testimonios",className:"testimonials","aria-labelledby":"testimonios-title",dangerouslySetInnerHTML:{__html:testimonialContent}}),o.jsx(tr,{})')
p.write_text(s, encoding='utf-8')
