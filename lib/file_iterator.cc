/* SPDX-License-Identifier: BSD-2-Clause
 *
 * This file is part of pyosmium. (https://osmcode.org/pyosmium/)
 *
 * Copyright (C) 2024 Sarah Hoffmann <lonvia@denofr.de> and others.
 * For a full list of authors see the git log.
 */
#include <pybind11/pybind11.h>

#include <osmium/io/any_input.hpp>
#include <osmium/io/file.hpp>

#include "osmium_module.h"
#include "base_handler.h"
#include "osm_base_objects.h"
#include "handler_chain.h"

namespace py = pybind11;

namespace {

class OsmFileIterator
{
public:
    OsmFileIterator(osmium::io::Reader *reader, py::args args)
    : m_reader(reader), m_handler(args)
    {
        m_buffer = m_reader->read();

        if (m_buffer) {
            m_buffer_it = m_buffer.begin();
        }
    }

    pybind11::object next()
    {
        while (true) {
            m_current.emplace<bool>(false);

            if (!m_buffer) {
                throw pybind11::stop_iteration();
            }

            while (m_buffer_it == m_buffer.end()) {
                m_buffer = m_reader->read();
                if (!m_buffer) {
                    m_handler.flush();
                    throw pybind11::stop_iteration();
                }
                m_buffer_it = m_buffer.begin();
            }

            osmium::OSMEntity *entity = &*m_buffer_it;
            ++m_buffer_it;

            switch (entity->type()) {
                case osmium::item_type::node:
                {
                    auto &obj = m_current.emplace<pyosmium::PyOSMNode>(entity);
                    if (!m_handler.node(obj)) {
                        return obj.get_or_create_python_object();
                    }
                    break;
                }
                case osmium::item_type::way:
                {
                    auto &obj = m_current.emplace<pyosmium::PyOSMWay>(entity);
                    if (!m_handler.way(obj)) {
                        return obj.get_or_create_python_object();
                    }
                    break;
                }
                case osmium::item_type::relation:
                {
                    auto &obj = m_current.emplace<pyosmium::PyOSMRelation>(entity);
                    if (!m_handler.relation(obj)) {
                        return obj.get_or_create_python_object();
                    }
                    break;
                }
                case osmium::item_type::area:
                {
                    auto &obj = m_current.emplace<pyosmium::PyOSMArea>(entity);
                    if (!m_handler.area(obj)) {
                        return obj.get_or_create_python_object();
                    }
                    break;
                }
                case osmium::item_type::changeset:
                {
                    auto &obj = m_current.emplace<pyosmium::PyOSMChangeset>(entity);
                    if (!m_handler.changeset(obj)) {
                        return obj.get_or_create_python_object();
                    }
                    break;
                }
                default:
                    break;
            }
       }

       return pybind11::object();
    }

private:
    osmium::io::Reader *m_reader;
    osmium::memory::Buffer m_buffer;
    osmium::memory::Buffer::iterator m_buffer_it;
    pyosmium::PyOSMAny m_current;

    pyosmium::HandlerChain m_handler;
};

} // namespace

namespace pyosmium {

void init_osm_file_iterator(py::module &m)
{
    py::class_<OsmFileIterator>(m, "OsmFileIterator",
        "Iterator interface for reading an OSM file.")
        .def(py::init<osmium::io::Reader *, py::args>(),
             py::keep_alive<0, 1>())
        .def("__iter__", [](py::object const &self) { return self; })
        .def("__next__", &OsmFileIterator::next,
             "Get the next OSM object from the file or raise a StopIteration.")
        ;
}

} // namespace
