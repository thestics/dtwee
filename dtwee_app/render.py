import functools

import jinja2
from django import http
from django.template import loader, engines, backends
from django.template.backends.utils import csrf_input_lazy, csrf_token_lazy


# credit: Alexandr Solovyov
@functools.cache
def macro_t(template_name, macro_name):
    jinja = next(e for e in engines.all()
                 if isinstance(e, backends.jinja2.Jinja2))
    return jinja.env.from_string(
        '{%% from "%s" import %s with context %%}{{ %s(**ctx) }}'
        % (template_name, macro_name, macro_name))


def render_macro(request, template_name, macro_name, extra_ctx=None, **ctx):
    jinja = next(e for e in engines.all()
                 if isinstance(e, backends.jinja2.Jinja2))
    extra_ctx = extra_ctx if extra_ctx is not None else {}
    reqctx = {
        "ctx": ctx,
        "request": request,
        "csrf_input": csrf_input_lazy(request),
        "csrf_token": csrf_token_lazy(request),
        **extra_ctx
    }
    for context_processor in jinja.template_context_processors:
        reqctx.update(context_processor(request))

    t = macro_t(template_name, macro_name)
    markup = t.render(reqctx)
    return http.HttpResponse(markup)
