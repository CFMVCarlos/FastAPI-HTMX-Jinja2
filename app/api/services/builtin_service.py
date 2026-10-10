from typing import Optional, List
import html
import random

class BuiltinService:
    def get_colored_paragraph(self, color: str) -> str:
        safe_color = html.escape(color)
        return f'<p id="p1" class="mb-4 text-lg font-semibold transition-colors duration-300 {safe_color}">This is my HTML template.</p>'

    def get_new_element(self) -> str:
        return """
            <p class="fade-me-in text-zinc-700 bg-zinc-100 p-4 rounded-lg my-2">This is a new element.</p>
            <div id="message" hx-swap-oob="true" class="bg-green-50 text-green-700 p-4 rounded-lg text-center mb-6 border border-green-200">Swap me directly using hx-swap-oob in the response!</div>
        """

    def get_select_elements(self) -> str:
        return """
            <p id="select_p" class="text-zinc-600">Paragraph</p>
            <div id="select_div" class="bg-zinc-100 p-4 rounded-lg my-2 text-zinc-700">Div</div>
            <h id="select_h" class="text-xl font-bold text-zinc-800">Header</h>
        """

    def get_select_elements_oob(self) -> str:
        return """
            <p id="select_p" class="text-zinc-600">Paragraph</p>
            <p id="p1" class="text-blue-600 font-semibold mb-4">This paragraph was changed using hx-select-oob in the request</p>
            <div id="select_div" class="bg-zinc-100 p-4 rounded-lg my-2 text-zinc-700">Div</div>
            <h1 id="select_h1" class="text-4xl font-extrabold tracking-tight text-red-600 transition-colors duration-500">Header was changed</h1>
            <span id="select_button_oob" class="inline-block px-4 py-2 bg-zinc-200 text-zinc-600 font-medium rounded-lg shadow-sm">Button Swapped</span>
        """
        
    def process_include(self, value: str) -> str:
        escaped_value = html.escape(value)
        return f'<div class="bg-blue-50 text-blue-700 p-4 rounded-lg my-2">Include information ({escaped_value})</div>'
