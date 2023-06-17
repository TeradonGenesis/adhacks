import {
  Box,
  Table as MuiTable,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  styled,
} from "@mui/material";
import React from "react";

const HeaderCell = styled(TableCell)(({ theme }) => ({
  backgroundColor: theme.palette.grey[300],
  color: theme.palette.grey[800],
  fontWeight: "bold",
}));

const Table = ({}) => {
  const columns = [
    { name: "Name" },
    { name: "Industry type" },
    { name: "Campaigns generated" },
  ];

  const data = [
    { id: 1 },
    { id: 2 },
    { id: 3 },
    { id: 4 },
    { id: 5 },
    { id: 6 },
  ];

  return (
    <Box sx={{ position: "relative" }}>
      <MuiTable stickyHeader>
        <TableHead>
          <TableRow>
            {columns.map((column) => (
              <HeaderCell key={column.name}>{column.name}</HeaderCell>
            ))}
          </TableRow>
        </TableHead>

        <TableBody>
          {data.map((data) => {
            return (
              <TableRow key={data.id}>
                {columns.map((column) => {
                  return (
                    <TableCell key={`${column.name}-${data.id}`}>
                      hahahahaa
                    </TableCell>
                  );
                })}
              </TableRow>
            );
          })}
        </TableBody>
      </MuiTable>
    </Box>
  );
};

export default Table;
