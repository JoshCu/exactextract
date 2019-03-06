// Copyright (c) 2019 ISciences, LLC.
// All rights reserved.
//
// This software is licensed under the Apache License, Version 2.0 (the "License").
// You may not use this file except in compliance with the License. You may
// obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef EXACTEXTRACT_GDAL_WRITER_H
#define EXACTEXTRACT_GDAL_WRITER_H

#include "output_writer.h"

namespace exactextract {

    class GDALWriter : public OutputWriter {

    public:
        GDALWriter(const std::string & filename, const std::string & id_field);

        ~GDALWriter();

        static std::string get_driver_name(const std::string & filename);

        void add_operation(const Operation & op) override;

        void set_registry(const StatsRegistry* reg) override;

        void write(const std::string & fid) override;

    private:
        using GDALDatasetH = void*;
        using OGRLayerH = void*;

        GDALDatasetH m_dataset;
        OGRLayerH m_layer;
        const StatsRegistry* m_reg;
    };

}

#endif //EXACTEXTRACT_GDAL_WRITER_H
