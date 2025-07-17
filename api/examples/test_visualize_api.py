"""可視化APIのテストスクリプト."""

import requests

# APIのベースURL
BASE_URL = "http://localhost:8000"


def test_simple_visualization() -> None:
    """シンプルなコードの可視化をテスト."""
    print("=== シンプルなコードの可視化テスト ===")

    payload = {
        "code": """x = 5
y = 10
z = x + y
print(f"結果: {z}")""",
        "highlight_line": 3,
        "show_memory": True,
    }

    response = requests.post(f"{BASE_URL}/api/v1/visualize", json=payload, timeout=10)

    if response.status_code == 200:  # noqa: PLR2004
        result = response.json()
        print(f"ステータス: {result['status']}")
        print(f"実行ステップ数: {len(result.get('steps', []))}")
        print(f"最終変数: {result.get('variables', {})}")
        print(f"説明: {result.get('explanation', '')}")

        # SVG が生成されているか確認
        if result.get("flow_diagram"):
            print("✓ フロー図が生成されました")
        if result.get("memory_diagram"):
            print("✓ メモリ図が生成されました")
    else:
        print(f"エラー: {response.status_code}")
        print(response.text)


def test_loop_visualization() -> None:
    """ループを含むコードの可視化をテスト."""
    print("\n=== ループを含むコードの可視化テスト ===")

    payload = {
        "code": """total = 0
for i in range(5):
    total += i
print(f"合計: {total}")""",
        "highlight_line": 0,
        "show_memory": True,
    }

    response = requests.post(f"{BASE_URL}/api/v1/visualize", json=payload, timeout=10)

    if response.status_code == 200:  # noqa: PLR2004
        result = response.json()
        print(f"ステータス: {result['status']}")
        print(f"説明: {result.get('explanation', '')}")

        # フロー図をファイルに保存
        if result.get("flow_diagram"):
            with open("api_flow_diagram.svg", "w", encoding="utf-8") as f:  # noqa: PTH123
                f.write(result["flow_diagram"])
            print("✓ フロー図を api_flow_diagram.svg に保存しました")
    else:
        print(f"エラー: {response.status_code}")
        print(response.text)


def test_error_visualization() -> None:
    """エラーを含むコードの可視化をテスト."""
    print("\n=== エラーを含むコードの可視化テスト ===")

    payload = {
        "code": """x = 10
y = 0
z = x / y  # ゼロ除算エラー""",
        "highlight_line": 3,
        "show_memory": False,
    }

    response = requests.post(f"{BASE_URL}/api/v1/visualize", json=payload, timeout=10)

    if response.status_code == 200:  # noqa: PLR2004
        result = response.json()
        print(f"ステータス: {result['status']}")

        if result.get("steps"):
            last_step = result["steps"][-1]
            if last_step.get("error"):
                print(f"検出されたエラー: {last_step['error']}")
    else:
        print(f"エラー: {response.status_code}")
        print(response.text)


def test_health_check() -> None:
    """APIのヘルスチェック."""
    print("\n=== APIヘルスチェック ===")

    response = requests.get(f"{BASE_URL}/", timeout=10)

    if response.status_code == 200:  # noqa: PLR2004
        result = response.json()
        print(f"ステータス: {result['status']}")
        print(f"バージョン: {result['version']}")
        print(f"メッセージ: {result['message']}")
    else:
        print(f"エラー: {response.status_code}")


if __name__ == "__main__":
    test_health_check()
    test_simple_visualization()
    test_loop_visualization()
    test_error_visualization()
