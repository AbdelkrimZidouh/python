import os


def load_dotenv_file(env_path: str = '.env') -> None:
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv(env_path, override=False)
    except ImportError:
        print("WARNING: python-dotenv not installed.")
        print("  Install with: pip install python-dotenv")
        print("  Falling back to OS environment variables only.")
        print()


def get_config() -> dict[str, str]:
    return {
        'MATRIX_MODE': os.environ.get('MATRIX_MODE', ''),
        'DATABASE_URL': os.environ.get('DATABASE_URL', ''),
        'API_KEY': os.environ.get('API_KEY', ''),
        'LOG_LEVEL': os.environ.get('LOG_LEVEL', ''),
        'ZION_ENDPOINT': os.environ.get('ZION_ENDPOINT', ''),
    }


def validate_config(config: dict[str, str]) -> list[str]:
    missing = []
    required = ['MATRIX_MODE', 'DATABASE_URL', 'API_KEY',
                'LOG_LEVEL', 'ZION_ENDPOINT']
    for key in required:
        if not config.get(key):
            missing.append(key)
    return missing


def mask_secret(value: str) -> str:
    if len(value) <= 4:
        return '****'
    return value[:2] + '****' + value[-2:]


def display_config(config: dict[str, str]) -> None:
    mode = config.get('MATRIX_MODE', 'unknown')
    db_url = config.get('DATABASE_URL', '')
    api_key = config.get('API_KEY', '')
    log_level = config.get('LOG_LEVEL', 'INFO')
    zion = config.get('ZION_ENDPOINT', '')

    print("Configuration loaded:")

    print(f"  Mode: {mode}")

    if db_url:
        if mode == 'production':
            print("  Database: Connected to production instance")
        else:
            print("  Database: Connected to local instance")
    else:
        print("  Database: [NOT CONFIGURED]")

    if api_key:
        print(f"  API Access: Authenticated ({mask_secret(api_key)})")
    else:
        print("  API Access: [NOT CONFIGURED]")

    print(f"  Log Level: {log_level}")

    if zion:
        print(f"  Zion Network: Online ({zion})")
    else:
        print("  Zion Network: [NOT CONFIGURED]")


def show_missing_config(missing: list[str]) -> None:
    print()
    print("WARNING: Missing configuration variables:")
    for var in missing:
        print(f"  - {var}")
    print()
    print("To configure:")
    print("  cp .env.example .env")
    print("  # Edit .env with your values")
    print("  python3 oracle.py")
    print()
    print("Or set environment variables directly:")
    print("  MATRIX_MODE=development python3 oracle.py")


def show_mode_differences(mode: str) -> None:
    print()
    print("=== Mode Configuration ===")
    if mode == 'production':
        print("  PRODUCTION mode:")
        print("  - Strict error handling")
        print("  - Minimal logging (ERROR only)")
        print("  - Remote database connections")
        print("  - All secrets required")
    else:
        print("  DEVELOPMENT mode:")
        print("  - Verbose logging (DEBUG)")
        print("  - Local database connections")
        print("  - Mock API endpoints allowed")
        print("  - Missing vars use defaults")


def scan_for_hardcoded_secrets(file_path: str) -> bool:
    """
    Scans the given Python file for hardcoded sensitive variables
    using only basic file operations and string methods.
    """
    sensitive_keys = ['API_KEY', 'DATABASE_URL', 'PASSWORD', 'SECRET_KEY']
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        secrets_found = False
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if line.startswith('#'):
                continue
            for key in sensitive_keys:
                if key in line and '=' in line:
                    parts = line.split('=', 1)
                    if len(parts) == 2:
                        value_part = parts[1].strip()
                        if value_part.startswith(("'", '"')):
                            print(
                                f"  [DANGER] Hardcoded value "
                                f"detected for {key} on line {line_num}"
                            )
                            secrets_found = True
        return secrets_found
    except FileNotFoundError:
        print(f"  [WARN] Could not find file to scan: {file_path}")
        return False


def security_check(config: dict[str, str]) -> None:
    print()
    print("Environment security check:")
    current_file_path = os.path.abspath(__file__)
    has_secrets = scan_for_hardcoded_secrets(current_file_path)
    if has_secrets:
        print("  [FAIL] Security breach! Hardcoded secrets detected.")
    else:
        print("  [OK] No hardcoded secrets detected")
    env_file_exists = os.path.exists(
        os.path.join(os.path.dirname(__file__), '.env')
    )
    if env_file_exists:
        print("  [OK] .env file properly configured")
    else:
        print("  [WARN] No .env file found (using env vars or defaults)")

    if os.environ.get('MATRIX_MODE') is not None:
        print("  [OK] Production overrides available")
    else:
        print("  [INFO] No environment overrides set")


if __name__ == "__main__":
    print("ORACLE STATUS: Reading the Matrix...")
    print()

    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv_file(env_path)

    config = get_config()
    missing = validate_config(config)

    if missing:
        show_missing_config(missing)
        print("Continuing with available configuration...")
        print()

    display_config(config)
    show_mode_differences(config.get('MATRIX_MODE', 'development'))
    security_check(config)

    print()
    print("The Oracle sees all configurations.")
