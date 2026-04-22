import sys
import importlib.util


def check_dependency(package: str) -> tuple[bool, str]:
    spec = importlib.util.find_spec(package)
    if spec is None:
        return False, "NOT FOUND"
    try:
        mod = importlib.import_module(package)
        version = getattr(mod, '__version__', 'unknown')
        return True, version
    except ImportError:
        return False, "NOT FOUND"


def show_dependency_status() -> dict[str, bool]:
    packages = {
        "pandas": "Data manipulation ready",
        "numpy": "Numerical computation ready",
        "matplotlib": "Visualization ready",
    }
    print("Checking dependencies:")
    available: dict[str, bool] = {}
    for pkg, desc in packages.items():
        ok, version = check_dependency(pkg)
        if ok:
            print(f"  [OK] {pkg} ({version}) - {desc}")
            available[pkg] = True
        else:
            print(f"  [MISSING] {pkg} - {desc}")
            available[pkg] = False
    return available


def show_install_instructions() -> None:
    print()
    print("Some dependencies are missing.")
    print("Install with pip:")
    print("  pip install -r requirements.txt")
    print()
    print("Install with Poetry:")
    print("  poetry install")
    print("  poetry run python loading.py")


def show_package_manager_comparison() -> None:
    print()
    print("=== pip vs Poetry ===")
    print("pip:")
    print("  - Manual dependency management")
    print("  - requirements.txt pinned versions")
    print("  - No lock file by default")
    print()
    print("Poetry:")
    print("  - Automatic dependency resolution")
    print("  - pyproject.toml + poetry.lock")
    print("  - Isolated virtual env management")


def run_analysis() -> None:
    import numpy as np
    import pandas as pd  # type: ignore
    import matplotlib  # type: ignore
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt  # type: ignore

    print("Analyzing Matrix data...")
    n_points = 1000
    print(f"Processing {n_points} data points...")

    np.random.seed(42)
    time = np.arange(n_points)
    signal = np.sin(time * 0.05) + np.random.normal(0, 0.2, n_points)
    noise = np.random.normal(0, 0.5, n_points)

    df = pd.DataFrame({
        'time': time,
        'signal': signal,
        'noise': noise,
        'combined': signal + noise * 0.3
    })

    mean_val = df['signal'].mean()
    std_val = df['signal'].std()
    print(f"  Signal mean: {mean_val:.4f}")
    print(f"  Signal std:  {std_val:.4f}")

    print("Generating visualization...")
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    axes[0].plot(df['time'][:200], df['signal'][:200],
                 color='green', linewidth=0.8, label='Matrix signal')
    axes[0].plot(df['time'][:200], df['combined'][:200],
                 color='red', alpha=0.5, linewidth=0.6, label='Combined')
    axes[0].set_title('Matrix Signal Analysis')
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel('Amplitude')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].hist(df['signal'], bins=50, color='green',
                 alpha=0.7, edgecolor='black')
    axes[1].set_title('Signal Distribution')
    axes[1].set_xlabel('Value')
    axes[1].set_ylabel('Frequency')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    output_file = 'matrix_analysis.png'
    plt.savefig(output_file, dpi=100, bbox_inches='tight')
    plt.close()

    print()
    print("Analysis complete!")
    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    print("LOADING STATUS: Loading programs...")
    print()

    available = show_dependency_status()

    all_ok = all(available.values())

    if not all_ok:
        show_install_instructions()
        show_package_manager_comparison()
        sys.exit(1)

    print()
    run_analysis()
    show_package_manager_comparison()
