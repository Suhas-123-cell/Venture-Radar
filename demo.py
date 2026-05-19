import gradio as gr
from dotenv import load_dotenv
from crew import run_discovery

load_dotenv()

EXAMPLES = ["logistics", "legal services", "construction", "healthcare billing", "HR & recruitment"]


def analyze(industry: str):
    if not industry.strip():
        yield "Please enter an industry name."
        return
    yield "Running 4 agents — this takes 60-90 seconds...\n\n*(Researcher → Competitor Scanner → Strategist → Brief Writer)*"
    try:
        result = run_discovery(industry.strip())
        yield result
    except Exception as e:
        yield f"Error: {str(e)}"


with gr.Blocks(title="VentureRadar", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# VentureRadar")
    gr.Markdown(
        "Type a B2B industry. Four autonomous agents research it, scan the competitive landscape, "
        "score opportunities, and produce ranked product briefs — ready to show a client or investor."
    )

    with gr.Row():
        industry_input = gr.Textbox(
            label="Industry",
            placeholder="e.g. logistics, legal, construction, healthcare billing...",
            scale=4,
        )
        run_btn = gr.Button("Run Discovery", variant="primary", scale=1)

    output = gr.Markdown(label="Discovery Report")

    run_btn.click(fn=analyze, inputs=[industry_input], outputs=[output])
    industry_input.submit(fn=analyze, inputs=[industry_input], outputs=[output])

    gr.Examples(examples=EXAMPLES, inputs=industry_input)

if __name__ == "__main__":
    demo.launch()
