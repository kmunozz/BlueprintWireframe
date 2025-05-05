import requests

def get_llama3_wireframe(prompt):
    url = "http://localhost:11434/api/chat"

    data = {
        "model": "llama3",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert in generating wireframes in draw.io (diagrams.net) format. "
                    "When given a UI prompt, return ONLY valid draw.io XML wrapped in <mxfile> tags. "
                    "Each <mxfile> must contain a <diagram> tag, and inside it a complete <mxGraphModel> block. "
                    "Within that block, include a <root> element with: "
                    "- <mxCell id='0'/> "
                    "- <mxCell id='1' parent='0'/> "
                    "- Additional <mxCell> elements with 'vertex=\"1\"', parent='1', and style attributes. "
                    "Each shape should use the <mxGeometry> tag to define x, y, width, height. "
                    "Use styles like 'rounded=1;fillColor=#f0f0f0;'. "
                    "Do NOT include markdown, explanation, or anything else. Only raw XML."
                )
            },
            {
                "role": "user",
                "content": "A simple homepage with a logo, a search bar, and a product grid"
            },
            {
                "role": "assistant",
                "content": """<mxfile host="app.diagrams.net">
<diagram name="Page-1">
<mxGraphModel>
<root>
  <mxCell id="0"/>
  <mxCell id="1" parent="0"/>
  <mxCell id="2" value="Logo" style="ellipse;fillColor=#FFFFFF;" vertex="1" parent="1">
    <mxGeometry x="30" y="25" width="100" height="40" as="geometry"/>
  </mxCell>
  <mxCell id="3" value="Search Bar" style="rounded=1;fillColor=#f0f0f0;" vertex="1" parent="1">
    <mxGeometry x="160" y="30" width="200" height="30" as="geometry"/>
  </mxCell>
  <mxCell id="4" value="Product Grid" style="rounded=1;fillColor=#e5e5e5;" vertex="1" parent="1">
    <mxGeometry x="25" y="90" width="400" height="300" as="geometry"/>
  </mxCell>
</root>
</mxGraphModel>
</diagram>
</mxfile>"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    response = requests.post(url, json=data)
    response.raise_for_status()
    result = response.json()
    return result["message"]["content"]
