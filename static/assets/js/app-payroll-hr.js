/**
 * App Payroll Employee Details (jquery)
 */

'use strict';

$(function () {
  // Variable declarations for tables
  var dt_payroll_table = $('.payroll-list-table');
  var dt_payroll_calendar_table = $('.payroll-calendar-table');
  var dt_deductions_contributions_table = $('.deductions-contributions-table');

  var dummyPayrollData = [
    {
      "employee_name": "John Doe",
      "employee_id": "123456",
      "department": "Sales",
      "position": "Sales Manager",
      "current_salary": "$5,000",
      "bonuses": "$500",
      "incentives": "$200",
      "pay_history": "January 2024: Salary increased to $5,000<br>December 2023: Year-end bonus of $500"
    },
    {
      "employee_name": "Jane Smith",
      "employee_id": "234567",
      "department": "Marketing",
      "position": "Marketing Analyst",
      "current_salary": "$4,200",
      "bonuses": "$400",
      "incentives": "$0",
      "pay_history": "February 2024: Performance bonus of $400<br>January 2024: Salary remains at $4,200"
    },
    {
      "employee_name": "Michael Johnson",
      "employee_id": "345678",
      "department": "Operations",
      "position": "Operations Lead",
      "current_salary": "$4,800",
      "bonuses": "$600",
      "incentives": "$300",
      "pay_history": "January 2024: Salary increased to $4,800<br>December 2023: Year-end bonus of $600"
    },
    {
      "employee_name": "Emily Davis",
      "employee_id": "456789",
      "department": "Finance",
      "position": "Financial Analyst",
      "current_salary": "$4,500",
      "bonuses": "$450",
      "incentives": "$150",
      "pay_history": "March 2024: Salary increased to $4,500<br>February 2024: Performance bonus of $450"
    },
    {
      "employee_name": "David Wilson",
      "employee_id": "567890",
      "department": "Human Resources",
      "position": "HR Manager",
      "current_salary": "$5,200",
      "bonuses": "$520",
      "incentives": "$220",
      "pay_history": "April 2024: Salary increased to $5,200<br>March 2024: Performance bonus of $520"
    },
    {
      "employee_name": "Sophia Brown",
      "employee_id": "678901",
      "department": "Sales",
      "position": "Sales Associate",
      "current_salary": "$3,800",
      "bonuses": "$380",
      "incentives": "$180",
      "pay_history": "May 2024: Salary increased to $3,800<br>April 2024: Performance bonus of $380"
    },
    {
      "employee_name": "James Miller",
      "employee_id": "789012",
      "department": "Marketing",
      "position": "Marketing Specialist",
      "current_salary": "$4,000",
      "bonuses": "$400",
      "incentives": "$0",
      "pay_history": "June 2024: Salary remains at $4,000<br>May 2024: Performance bonus of $400"
    },
    {
      "employee_name": "Ava Taylor",
      "employee_id": "890123",
      "department": "Operations",
      "position": "Operations Coordinator",
      "current_salary": "$4,600",
      "bonuses": "$460",
      "incentives": "$260",
      "pay_history": "July 2024: Salary increased to $4,600<br>June 2024: Performance bonus of $460"
    },
    {
      "employee_name": "William Martinez",
      "employee_id": "901234",
      "department": "Finance",
      "position": "Accountant",
      "current_salary": "$4,700",
      "bonuses": "$470",
      "incentives": "$170",
      "pay_history": "August 2024: Salary increased to $4,700<br>July 2024: Performance bonus of $470"
    },
    {
      "employee_name": "Olivia Anderson",
      "employee_id": "012345",
      "department": "Human Resources",
      "position": "HR Specialist",
      "current_salary": "$4,900",
      "bonuses": "$490",
      "incentives": "$190",
      "pay_history": "September 2024: Salary increased to $4,900<br>August 2024: Performance bonus of $490"
    }
  ];

  var dummyCalendarData = [
    {
      "pay_period": "01/01/2024 - 01/15/2024",
      "payment_date": "01/20/2024",
      "status": "Processed"
    },
    {
      "pay_period": "01/16/2024 - 01/31/2024",
      "payment_date": "02/05/2024",
      "status": "Pending"
    },
    {
      "pay_period": "02/01/2024 - 02/15/2024",
      "payment_date": "02/20/2024",
      "status": "Scheduled"
    },
    {
      "pay_period": "02/16/2024 - 02/29/2024",
      "payment_date": "03/05/2024",
      "status": "Pending"
    },
    {
      "pay_period": "03/01/2024 - 03/15/2024",
      "payment_date": "03/20/2024",
      "status": "Processed"
    },
    {
      "pay_period": "03/16/2024 - 03/31/2024",
      "payment_date": "04/05/2024",
      "status": "Scheduled"
    },
    {
      "pay_period": "04/01/2024 - 04/15/2024",
      "payment_date": "04/20/2024",
      "status": "Processed"
    },
    {
      "pay_period": "04/16/2024 - 04/30/2024",
      "payment_date": "05/05/2024",
      "status": "Pending"
    },
    {
      "pay_period": "05/01/2024 - 05/15/2024",
      "payment_date": "05/20/2024",
      "status": "Scheduled"
    },
    {
      "pay_period": "05/16/2024 - 05/31/2024",
      "payment_date": "06/05/2024",
      "status": "Processed"
    }
  ];

  var dummyDeductionsData = [
    {
      "employee_name": "John Doe",
      "employee_id": "123456",
      "taxes": "$1,000",
      "benefits_deductions": "$300",
      "employer_contributions": "$200"
    },
    {
      "employee_name": "Jane Smith",
      "employee_id": "234567",
      "taxes": "$800",
      "benefits_deductions": "$250",
      "employer_contributions": "$150"
    },
    {
      "employee_name": "Michael Johnson",
      "employee_id": "345678",
      "taxes": "$900",
      "benefits_deductions": "$270",
      "employer_contributions": "$180"
    },
    {
      "employee_name": "Emily Davis",
      "employee_id": "456789",
      "taxes": "$850",
      "benefits_deductions": "$260",
      "employer_contributions": "$170"
    },
    {
      "employee_name": "David Wilson",
      "employee_id": "567890",
      "taxes": "$1,050",
      "benefits_deductions": "$320",
      "employer_contributions": "$210"
    },
    {
      "employee_name": "Sophia Brown",
      "employee_id": "678901",
      "taxes": "$760",
      "benefits_deductions": "$230",
      "employer_contributions": "$150"
    },
    {
      "employee_name": "James Miller",
      "employee_id": "789012",
      "taxes": "$800",
      "benefits_deductions": "$250",
      "employer_contributions": "$160"
    },
    {
      "employee_name": "Ava Taylor",
      "employee_id": "890123",
      "taxes": "$920",
      "benefits_deductions": "$280",
      "employer_contributions": "$190"
    },
    {
      "employee_name": "William Martinez",
      "employee_id": "901234",
      "taxes": "$940",
      "benefits_deductions": "$290",
      "employer_contributions": "$195"
    },
    {
      "employee_name": "Olivia Anderson",
      "employee_id": "012345",
      "taxes": "$980",
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
        { data: 'department', title: 'Department', render: function(data) { return getDepartmentBadge(data); } },
        { data: 'position', title: 'Position', render: function(data) { return getPositionBadge(data); } },
        { data: 'current_salary', title: 'Current Salary ($)' },
        { data: 'bonuses', title: 'Bonuses ($)' },
        { data: 'incentives', title: 'Incentives ($)' },
        { data: 'pay_history', title: 'Pay History', render: function(data) { return data.replace(/\n/g, '<br>'); } }
      ]
    });
  }

  // Code to render the payroll calendar table with dummy data
  if (dt_payroll_calendar_table.length) {
    dt_payroll_calendar_table.DataTable({
      data: dummyCalendarData,
      columns: [
        { data: 'pay_period', title: 'Pay Period' },
        { data: 'payment_date', title: 'Payment Date' },
        { data: 'status', title: 'Status', render: function(data) { return getStatusBadge(data); } }
      ]
    });
  }

  // Code to render the deductions and contributions table with dummy data
  if (dt_deductions_contributions_table.length) {
    dt_deductions_contributions_table.DataTable({
      data: dummyDeductionsData,
      columns: [
        { data: 'employee_name', title: 'Employee Name' },
        { data: 'employee_id', title: 'Employee ID' },
        { data: 'taxes', title: 'Taxes ($)' },
        { data: 'benefits_deductions', title: 'Benefits Deductions ($)' },
        { data: 'employer_contributions', title: 'Employer Contributions ($)' }
      ]
    });
  }
});
