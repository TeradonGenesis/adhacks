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

const Table = ({ onRowClick }) => {
  const columns = [
    { name: "Name", key: "name" },
    { name: "Industry type", key: "type" },
    { name: "Campaigns generated", key: "generatedCount" },
  ];

  const data = [
    { id: 1, name: "SME1", type: "Tourism", generatedCount: 11 },
    { id: 2, name: "SME2", type: "Health services", generatedCount: 0 },
    { id: 3, name: "Nandos", type: "Restaurant", generatedCount: 1 },
    { id: 4, name: "High Fashion brand", type: "Fashion", generatedCount: 9 },
    { id: 5, name: "SME3", type: "F&B", generatedCount: 11 },
    { id: 6, name: "SME4", type: "Education", generatedCount: 332 },
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
              <TableRow
                hover
                key={data.id}
                sx={{ cursor: "pointer" }}
                onClick={onRowClick}
              >
                {columns.map((column) => {
                  return (
                    <TableCell key={`${column.name}-${data.id}`}>
                      {data[column.key]}
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
