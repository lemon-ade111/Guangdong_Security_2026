import csv
import os
import re
import urllib.error
import urllib.request


INPUT_CSV = "/home/lemon/Guangdong_Security_2026/March_Foundation/scripts/intelligence.csv"
OUTPUT_TXT = "/home/lemon/Guangdong_Security_2026/March_Foundation/scripts/audit_results_0302.txt"

URL_REGEX = re.compile(
    r"^https?://"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+"
    r"(?:[/?#].*)?$"
)

RISK_KEYWORDS = ["漏洞", "Leak", "leak"]

CONTROL_WHITELIST = {"\t"}

PIPL_BASIS = "PIPL Article 51 – data integrity and security measures"


def has_unexpected_control_chars(text: str) -> bool:
    for ch in text:
        if ord(ch) < 32 and ch not in CONTROL_WHITELIST:
            return True
    return False


def is_url_reachable(url: str, timeout: float = 5.0) -> tuple[bool, str]:
    if not url:
        return False, "Empty URL"
    try:
        request = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(request, timeout=timeout) as response:
            code = response.getcode()
            if 200 <= code < 400:
                return True, f"HTTP {code}"
            return False, f"HTTP {code}"
    except urllib.error.HTTPError as exc:
        return False, f"HTTPError {exc.code}"
    except urllib.error.URLError as exc:
        return False, f"URLError {exc.reason}"
    except Exception as exc:
        return False, type(exc).__name__


def classify_row(title: str, url: str, raw: str) -> tuple[str, list[str]]:
    status = "[INFO]"
    reasons: list[str] = []

    in_title = title or ""
    for word in RISK_KEYWORDS:
        if word in in_title:
            status = "[HIGH RISK]"
            reasons.append("Title contains high-risk keyword")
            break

    url_text = url or ""
    if not URL_REGEX.match(url_text):
        status = "[HIGH RISK]"
        reasons.append("URL failed strict regex validation")
    else:
        ok, detail = is_url_reachable(url_text)
        if not ok:
            status = "[HIGH RISK]"
            reasons.append(f"URL not reachable: {detail}")

    if has_unexpected_control_chars(raw):
        status = "[HIGH RISK]"
        reasons.append("Unexpected control characters detected in row")

    if not reasons:
        reasons.append("Row passed integrity, format, and reachability checks")

    return status, reasons


def main() -> int:
    if not os.path.exists(INPUT_CSV):
        print(f"输入数据文件不存在: {INPUT_CSV}")
        return 1

    try:
        infile = open(INPUT_CSV, "r", encoding="utf-8")
    except OSError as exc:
        print(f"读取输入文件失败: {exc}")
        return 1

    try:
        outfile = open(OUTPUT_TXT, "w", encoding="utf-8")
    except OSError as exc:
        infile.close()
        print(f"写入结果文件失败: {exc}")
        return 1

    with infile, outfile:
        for line_number, raw in enumerate(infile, start=1):
            raw_stripped = raw.rstrip("\n")
            status = "[INFO]"
            reasons: list[str] = []
            try:
                reader = csv.reader([raw_stripped])
                row = next(reader, None)
                if not row or len(row) < 2:
                    status = "[MALFORMED DATA - TAMPERED]"
                    reasons.append("Missing required fields (title,url)")
                else:
                    title = row[0].strip()
                    url = row[1].strip()
                    status, reasons = classify_row(title, url, raw_stripped)
            except Exception as exc:
                status = "[MALFORMED DATA - TAMPERED]"
                reasons.append(f"CSV parsing error: {type(exc).__name__}")

            reason_str = "; ".join(reasons)
            report_line = (
                f"line={line_number} | status={status} | "
                f"reason={reason_str} | basis={PIPL_BASIS} | "
                f"raw={raw_stripped}"
            )
            outfile.write(report_line + "\n")

    print(f"审计完成，结果已写入: {OUTPUT_TXT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

