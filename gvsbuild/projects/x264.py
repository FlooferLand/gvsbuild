#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>.

import os

from gvsbuild.utils.base_expanders import GitRepo
from gvsbuild.utils.base_project import Project, project_add
from gvsbuild.utils.utils import convert_to_msys


@project_add
class X264(GitRepo, Project):
    def __init__(self):
        Project.__init__(
            self,
            "x264",
            repo_url="http://git.videolan.org/git/x264.git",
            fetch_submodules=False,
            dependencies=["nasm", "msys2"],
            tag="e9a5903edf8ca59ef20e6f4894c196f135af735e",
            patches=[
                "0001-use-more-recent-version-of-config.guess.patch",
                "0002-configure-recognize-the-msys-shell.patch",
            ],
        )

    def build(self):
        msys_path = Project.get_tool_path("msys2")
        self.exec_vs(
            r"%s\bash build\build.sh %s %s"
            % (
                msys_path,
                convert_to_msys(self.builder.gtk_dir),
                self.builder.opts.configuration,
            ),
            add_path=msys_path,
        )

        # use the path expected when building with a dependent project
        self.builder.exec_msys(
            ["mv", "libx264.dll.lib", "libx264.lib"],
            working_dir=os.path.join(self.builder.gtk_dir, "lib"),
        )

        self.install(r".\COPYING share\doc\x264")
