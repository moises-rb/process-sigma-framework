"""Utility functions for saving Plotly figures to disk."""
from pathlib import Path
from typing import Dict, Optional
import plotly.graph_objects as go
from plotly.basedatatypes import BaseFigure


def ensure_output_dir(path: Path) -> None:
    """Create the export directory if it does not exist."""
    path.mkdir(parents=True, exist_ok=True)


def save_figure(
    fig: BaseFigure,
    filename: str,
    output_dir: str = "exports",
    engine: str = "kaleido",
    format: Optional[str] = None,
) -> str:
    """Save a single Plotly figure to the exports folder.

    Args:
        fig: Plotly figure to save.
        filename: Output filename, with or without extension.
        output_dir: Directory where files are saved.
        engine: Plotly image engine to use.
        format: Optional explicit image format (png, jpg, svg, pdf).

    Returns:
        The path of the saved file.
    """
    output_path = Path(output_dir)
    ensure_output_dir(output_path)

    file_path = output_path / filename
    if format is not None:
        file_path = file_path.with_suffix(f".{format}")

    fig.write_image(str(file_path), engine=engine)
    return str(file_path)


def save_figures(
    figures: Dict[str, BaseFigure],
    output_dir: str = "exports",
    engine: str = "kaleido",
    format: Optional[str] = None,
) -> Dict[str, str]:
    """Save multiple Plotly figures using a filename-to-figure map.

    Args:
        figures: Mapping of output filename to Plotly figure.
        output_dir: Directory where files are saved.
        engine: Plotly image engine to use.
        format: Optional explicit image format for all figures.

    Returns:
        Mapping of input filenames to saved file paths.
    """
    saved_paths = {}
    for filename, fig in figures.items():
        saved_paths[filename] = save_figure(
            fig,
            filename,
            output_dir=output_dir,
            engine=engine,
            format=format,
        )
    return saved_paths
