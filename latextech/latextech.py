import subprocess
import os
from sys import argv
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

toks = {"s":512,"m":1024,"l":2048,"max":4096}


def latex_compile(path):
    try:
        subprocess.run(['pdflatex', path])
    except subprocess.CalledProcessError as err:
        print(f"LaTeX compilation failed with error: {err}")

role = r"""

You will be provided with a question, your job is to compile notes on said question.

! IMPORTANT !
    FOR MATH AND PHYSICS QUESTIONS PROVIDE EQUATIONS
    FOR PROGRAMING QUESTIONS PROVIDE CODE SAMPLES
! IMPORTANT !

All your writings must be in a .tex format, one that is able to be compiled with pdflatex.

! IMPORTANT !
Always begin the document with :
\documentclass{article}
\begin{document}
! IMPORTANT !

Be sure to add the appropriate '\usepackage' that are required for said notes.

Example input : "Explain Newton's first law"

Example output : 
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Newton's First Law}

Newton's first law, also known as the law of inertia, states that an object at rest will remain at rest, and an object in motion will continue in motion with a constant velocity unless acted upon by an external force.

\subsection*{Equations}

Here are some equations related to Newton's first law:

\begin{enumerate}
  \item The equation of motion for a particle under no external force:
  \begin{equation*}
    \sum F = 0
  \end{equation*}
  
  \item The equilibrium condition for forces acting on an object:
  \begin{equation*}
    \sum F_{\text{net}} = 0
  \end{equation*}
  
  \item The relationship between force, mass, and acceleration:
  \begin{equation*}
    F = m \cdot a
  \end{equation*}
\end{enumerate}

\end{document}

"""


prompt = input ("What notes would you like ? ")

tex_file_path = prompt.strip()+".tex"

notes = openai.Completion.create (
    engine = 'text-davinci-003',
    prompt = role + prompt,
    max_tokens = int(toks.get(argv[1])),
    n=1,
    temperature = 0.5

)

with open (tex_file_path,"w") as file :
    file.write(notes.choices[0].text.strip())
latex_compile(tex_file_path)
latex_file = prompt + ".pdf"
subprocess.run(['open',latex_file])
