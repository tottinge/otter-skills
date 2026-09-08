from timeouts import parse_timeout


def should_run(config):
    timeout = parse_timeout(config.get("timeout", ""))
    return timeout <= 0
