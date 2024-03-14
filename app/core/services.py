def extract_client_id(meta):

    if x_forwared_for := meta.get("HTTP_X_FORWARDED_FOR"):
        ip = x_forwared_for.split(",")[0].strip()
    else:
        ip = meta.get("REMOTE_ADDR")

    return ip
