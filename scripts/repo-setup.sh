#!/usr/bin/env bash
#
# Copyright (C) 2024 Gary Kim <gary@garykim.dev>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

set -euf -o pipefail

# This line will only work in scripts and not sourced bash scripts.
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
cd "$SCRIPTPATH/.."

# Configure Mailing List
git config format.subjectPrefix "PATCH gkjh"
git config sendemail.to '~gary-kim/gkjh-devel@lists.sr.ht'

# Git Notes
git config format.notes true
git config notes.rewriteRef ref/notes/commits
git config notes.rewriteMode concatenate

# Git Hooks
mkdir -p .git/hooks
rm -f .git/hooks/commit-msg
ln -s ../../scripts/pre-commit .git/hooks/commit-msg
