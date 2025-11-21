import os
from github import Github, Auth
from github.Gist import Gist
import json
from typing import Optional, Dict, Any

GIST_FILENAME = "es_architect_data.json"
GIST_DESCRIPTION = "ES Architect Data Backup"

class GitHubSync:
    def __init__(self, token: str):
        self.token = token
        auth = Auth.Token(token)
        self.g = Github(auth=auth)
        self.user = self.g.get_user()

    def _find_gist(self) -> Optional[Gist]:
        """Finds the specific gist for this app."""
        try:
            # Iterate through user's gists to find one with the specific filename
            for gist in self.user.get_gists():
                if GIST_FILENAME in gist.files:
                    return gist
            return None
        except Exception as e:
            print(f"Error finding gist: {e}")
            return None

    def upload_data(self, data: list[dict]) -> str:
        """Uploads (creates or updates) the ES data to Gist."""
        try:
            json_str = json.dumps(data, ensure_ascii=False, indent=2)
            gist = self._find_gist()
            
            if gist:
                # Update existing gist
                gist.edit(
                    description=GIST_DESCRIPTION,
                    files={GIST_FILENAME: {"content": json_str}}
                )
                return f"✅ 既存のバックアップを更新しました！ (ID: {gist.id})"
            else:
                # Create new gist
                new_gist = self.user.create_gist(
                    public=False,
                    files={GIST_FILENAME: {"content": json_str}},
                    description=GIST_DESCRIPTION
                )
                return f"✅ 新しいバックアップを作成しました！ (ID: {new_gist.id})"
        except Exception as e:
            return f"❌ アップロードエラー: {str(e)}"

    def download_data(self) -> tuple[Optional[list[dict]], str]:
        """Downloads data from Gist."""
        try:
            gist = self._find_gist()
            if not gist:
                return None, "⚠️ バックアップが見つかりませんでした。"
            
            file = gist.files[GIST_FILENAME]
            content = file.content
            data = json.loads(content)
            return data, "✅ バックアップを復元しました！"
        except Exception as e:
            return None, f"❌ ダウンロードエラー: {str(e)}"
