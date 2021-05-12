from yarl import URL


def urljoin(base_url: str, *urlpath) -> URL:
    path = [str(path).strip(' /') for path in urlpath if path]
    path = '/'.join(path)
    url = URL(base_url).with_path(path)
    return url
