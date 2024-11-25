# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Postgis(AutotoolsPackage):
    """
    PostGIS is a spatial database extender for PostgreSQL object-relational
    database. It adds support for geographic objects allowing location
    queries to be run in SQL
    """

    homepage = "https://postgis.net/"
    url = "https://download.osgeo.org/postgis/source/postgis-2.5.3.tar.gz"

    license("GPL-2.0-or-later")

    version("3.1.2", sha256="2cdd3760176926704b4eb25ff3357543c9637dee74425a49082906857c7e0732")
    version("3.0.1", sha256="5a5432f95150d9bae9215c6d1c7bb354e060482a7c379daa9b8384e1d03e6353")
    version("3.0.0", sha256="c06fd2cd5cea0119106ffe17a7235d893c2bbe6f4b63c8617c767630973ba594")
    version("2.5.3", sha256="72e8269d40f981e22fb2b78d3ff292338e69a4f5166e481a77b015e1d34e559a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "gui",
        default=False,
        description=(
            "Build with GUI support, creating shp2pgsql-gui graphical interface " "to shp2pgsql"
        ),
    )

    # Refs:
    # https://postgis.net/docs/postgis_installation.html
    # https://postgis.net/source/

    depends_on("postgresql")
    depends_on("geos")
    depends_on("proj")
    depends_on("gdal")
    depends_on("libxml2")
    depends_on("json-c")

    depends_on("sfcgal")
    depends_on("pcre")
    depends_on("perl", type=("build", "run"))
    depends_on("protobuf-c")

    depends_on("gtkplus@:2.24.32", when="+gui")

    def setup_build_environment(self, env):
        env.set("POSTGIS_GDAL_ENABLED_DRIVERS", "ENABLE_ALL")

    def setup_run_environment(self, env):
        env.set("POSTGIS_GDAL_ENABLED_DRIVERS", "ENABLE_ALL")

    def configure_args(self):
        args = []
        args.append("--with-sfcgal=" + str(self.spec["sfcgal"].prefix.bin) + "/sfcgal-config")
        args.append("--with-protobufdir=" + self.spec["protobuf-c"].prefix)
        if "+gui" in self.spec:
            args.append("--with-gui")
        return args

    @run_after("install")
    def satisfy_sanity_check(self):
        # sanity_check_prefix requires something in the install directory,
        # but PostGIS is installed in PostgreSQL's install directory.
        os.symlink(self.spec["postgresql"].prefix, self.prefix.postgresql)
