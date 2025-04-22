/**
 * App Payroll Employee Details (jquery)
 */

'use strict';

$(function () {
  // Variable declarations for tables
  var dt_payroll_table = $('.payroll-list-table');
  var dummyPayrollData = [
    {
      "employee_name": "John Doe",
      "employee_id": "123456",
      "current_salary": "$5,000",
      "bonuses": "$500",
      "incentives": "$200",
      "pay_history": "January 2024: Salary increased to $5,000<br>December 2023: Year-end bonus of $500",
      "taxes": "$1,000",
      "benefits_deductions": "$300",
      "employer_contributions": "$200"
    }
  ];

  function getDepartmentBadge(department) {
    switch(department) {
      case 'Sales':
        return '<span class="badge bg-primary">' + department + '</span>';
      case 'Marketing':
        return '<span class="badge bg-success">' + department + '</span>';
      case 'Operations':
        return '<span class="badge bg-warning">' + department + '</span>';
      case 'Finance':
        return '<span class="badge bg-danger">' + department + '</span>';
      case 'Human Resources':
        return '<span class="badge bg-info">' + department + '</span>';
      default:
        return '<span class="badge bg-secondary">' + department + '</span>';
    }
  }

  function getPositionBadge(position) {
    switch(position) {
        case 'Sales Manager':
          return '<span class="badge bg-primary">' + position + '</span>';
          case 'Sales Associate':
          return '<span class="badge bg-primary">' + position + '</span>';
        case 'Marketing Analyst':
          return '<span class="badge bg-success">' + position + '</span>';
        case 'Marketing Specialist':
            return '<span class="badge bg-success">' + position + '</span>';
        case 'Operations Lead':
          return '<span class="badge bg-warning">' + position + '</span>';
          case 'Operations Coordinator':
            return '<span class="badge bg-warning">' + position + '</span>';
        case 'Finance Manager':
          return '<span class="badge bg-danger">' + position + '</span>';
          case 'Accountant':
          return '<span class="badge bg-danger">' + position + '</span>';
          case 'Financial Analyst':
          return '<span class="badge bg-danger">' + position + '</span>';
        case 'HR Specialist':
          return '<span class="badge bg-info">' + position + '</span>';
          case 'HR Manager':
            return '<span class="badge bg-info">' + position + '</span>';
        default:
          return '<span class="badge bg-secondary">' + position + '</span>';
      }
  }

  function getStatusBadge(status) {
    switch(status) {
      case 'Processed':
        return '<span class="badge bg-success">' + status + '</span>';
      case 'Pending':
        return '<span class="badge bg-warning">' + status + '</span>';
      case 'Scheduled':
        return '<span class="badge bg-info">' + status + '</span>';
      default:
        return '<span class="badge bg-secondary">' + status + '</span>';
    }
  }

  // Code to render the payroll employee details table with dummy data
  if (dt_payroll_table.length) {
    dt_payroll_table.DataTable({
      data: dummyPayrollData,
      columns: [
        { data: 'employee_name', title: 'Employee Name' },
        { data: 'employee_id', title: 'Employee ID' },
        { data: 'current_salary', title: 'Current Salary ($)' },
        { data: 'bonuses', title: 'Bonuses ($)' },
        { data: 'incentives', title: 'Incentives ($)' },
        { data: 'pay_history', title: 'Pay History', render: function(data) { return data.replace(/\n/g, '<br>'); } },
        { data: 'taxes', title: 'Taxes ($)' },
        { data: 'benefits_deductions', title: 'Benefits Deductions ($)' },
        { data: 'employer_contributions', title: 'Employer Contributions ($)' }
      ]
    });
  }

});
