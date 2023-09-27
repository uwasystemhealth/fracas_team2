"use client";

/*
 * Better FRACAS
 * Copyright (C) 2023  Peter Tanner, ??? Better Fracas team
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

import DeleteConfirmation from "@/components/Dialogs/DeleteConfirmation";
import * as React from "react";
import {
  DataGrid,
  GridCellParams,
  GridColDef,
  GridValueGetterParams,
  MuiEvent,
} from "@mui/x-data-grid";
import TextField from "@mui/material/TextField";
import Card from "@mui/material/Card";
import IconButton from "@mui/material/IconButton";
import VisibilityIcon from "@mui/icons-material/Visibility";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import { boolean, date } from "yup";
import { useEffect, useState } from "react";
import { API_CLIENT, API_ENDPOINT, API_TYPES } from "@/helpers/api";
import { AxiosError, AxiosResponse } from "axios";

const disableSelectBtns = (
  params: GridCellParams,
  event: MuiEvent<React.MouseEvent>
) => {
  if (["edit", "view", "delete"].includes(params.field)) {
    event.stopPropagation();
    event.defaultMuiPrevented = true;
  }
};

export interface UserReport {
  id: number;
  created_at: string;
  title: string;
  creator: string;
  status: string;
}

export interface Props {
  rows: UserReport[];
  setRows: React.Dispatch<React.SetStateAction<UserReport[]>>;
}

export default function ReportList({ rows, setRows }: Props) {
  const [searchTerm, setSearchTerm] = React.useState("");
  const [showDeleteDialog, setShowDeleteDialog] = React.useState(false);
  const [deleteFunction, setDeleteFunction] = useState<
    React.MouseEventHandler<HTMLButtonElement> | undefined
  >(undefined);

  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "title", headerName: "Report name", flex: 1 },
    { field: "created_at", headerName: "Creation Date", flex: 1 },
    { field: "car_year", headerName: "Car year", flex: 1 },
    {
      field: "creator.name",
      headerName: "Creator name",
      flex: 1,
      valueGetter: (params) => params.row?.creator?.email,
    },
    {
      field: "edit",
      headerName: "Edit",
      width: 75,
      align: "center",
      headerAlign: "center",
      sortable: false,
      filterable: false,
      renderCell: (params) => (
        <IconButton
          color="primary"
          aria-label="Edit"
          href={`/editreport/${params.row.id}`}
        >
          <EditIcon />
        </IconButton>
      ),
    },
    {
      field: "view",
      headerName: "View",
      width: 75,
      align: "center",
      headerAlign: "center",
      sortable: false,
      filterable: false,
      renderCell: (params) => (
        <IconButton
          color="primary"
          aria-label="View"
          href={`/viewreport/${params.row.id}`}
        >
          <VisibilityIcon />
        </IconButton>
      ),
    },
    {
      field: "delete",
      headerName: "Delete",
      width: 75,
      align: "center",
      headerAlign: "center",
      sortable: false,
      filterable: false,
      renderCell: (params) => (
        <IconButton
          color="primary"
          aria-label="Delete"
          onClick={() => {
            setShowDeleteDialog(true);
            setDeleteFunction(() => () => {
              console.log(`Removed item ${params.row.id}`);
              setRows(rows.filter((item) => item.id !== params.row.id));
              (async () => {
                try {
                  const response = await API_CLIENT.delete(
                    `${API_ENDPOINT.RECORD}/${params.row.id}`
                  )
                    .then((response) => {})
                    .catch((error: AxiosError) => {
                      console.error("An error occurred " + error.message);
                    });
                } catch (error: any) {}
              })();
            });
          }}
          // href={`/viewreport/${params.row.id}`}
        >
          <DeleteIcon />
        </IconButton>
      ),
    },
  ];

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  };

  const filteredRows = rows.filter((row) =>
    Object.values(row).some((value) =>
      value?.toString().toLowerCase().includes(searchTerm.toLowerCase())
    )
  );

  return (
    <>
      <DeleteConfirmation
        open={showDeleteDialog}
        setOpen={setShowDeleteDialog}
        onDelete={deleteFunction}
      />
      <Card
        style={{
          padding: 10,
          maxWidth: "100%",
          margin: "0 auto",
        }}
      >
        <TextField
          label="Search"
          value={searchTerm}
          onChange={handleSearchChange}
          variant="outlined"
          fullWidth
          sx={{ marginBottom: 2 }}
        />
        <DataGrid
          rows={filteredRows}
          columns={columns}
          pagination
          pageSizeOptions={[5, 25, 100]}
          checkboxSelection
          onCellClick={disableSelectBtns}
          sortModel={[{ field: "created_at", sort: "desc" }]}
        />
      </Card>
    </>
  );
}
