\ProvidesClass{resume}
\LoadClass[11pt,letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage{hyperref}
\usepackage[letterpaper, portrait, margin=1in]{geometry}
\usepackage[shortlabels]{enumitem}
% \usepackage{multicols}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.6em}

\newcommand{\name}[1]{\hfil{\vspace{-0.5em}\bf\LARGE{#1}}\hfil\par}
\newcommand{\info}[2]{\hfil #1 \hspace{1em} #2\par}

\newcommand{\rsection}[1]{\textbf{#1} \vspace{0.2em} \hrule \par}
\newcommand{\rsubsection}[2]{\textbf{#1} \hfill #2\\}
\newcommand{\position}[2]{#1 \hfill #2 \\ \vspace{-1em}}

\newenvironment{LIST}{
	\vspace{-1.5em}
	\begin{itemize}[label=|,itemsep=-0.4em]
}
{
	\end{itemize}
	\vspace{-1em}
}
