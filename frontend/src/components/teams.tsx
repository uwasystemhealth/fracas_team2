/*
 * Better FRACAS
 * Copyright (C) 2023  ??? Better Fracas team
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

import React, { useEffect, useState } from "react";
import Typography from "@mui/material/Typography";
import { DataGrid, GridColDef, GridValueGetterParams } from '@mui/x-data-grid';
import axios from 'axios';

interface Team {
  id: number;
  team: string;
  leader: string;
}

const columns: GridColDef[] = [
  { field: 'id', headerName: 'ID', width: 70 },
  { field: 'team', headerName: 'Team', width: 200 },
  { field: 'leader', headerName: 'Leader', width: 200 },
];

const UserTable: React.FC = () => {
  const [teams, setTeams] = useState<Team[]>([]);

  useEffect(() => {
    // Make a GET request to your Flask backend to fetch the list of users
    axios.get('http://localhost:5000/api/v1/get/team_list')
      .then((response) => {
        setTeams(response.data);
      })
      .catch((error) => {
        console.error('Error fetching teams:', error);
      });
  }, []);

  return (
    <React.Fragment>
      <DataGrid
        rows={teams}
        columns={columns}
        initialState={{
          pagination: {
            paginationModel: { page: 0, pageSize: 5 },
          },
        }}
        pageSizeOptions={[5, 10]}
        checkboxSelection
      />
    </React.Fragment>
  );
}
export default UserTable;
