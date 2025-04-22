/**
 * Page User List
 */

'use strict';

// Datatable (jquery)
$(function () {
  let borderColor, bodyBg, headingColor;

  if (isDarkStyle) {
    borderColor = config.colors_dark.borderColor;
    bodyBg = config.colors_dark.bodyBg;
    headingColor = config.colors_dark.headingColor;
  } else {
    borderColor = config.colors.borderColor;
    bodyBg = config.colors.bodyBg;
    headingColor = config.colors.headingColor;
  }

  // Variable declaration for table
  var dt_user_table = $('.datatables-users'),
    select2 = $('.select2'),
    userView = 'app-user-view-account.html',
    statusObj = {
      1: { title: 'Pending', class: 'bg-label-warning' },
      2: { title: 'Active', class: 'bg-label-success' },
      3: { title: 'Inactive', class: 'bg-label-secondary' }
    };

  if (select2.length) {
    var $this = select2;
    $this.wrap('<div class="position-relative"></div>').select2({
      placeholder: 'Select Country',
      dropdownParent: $this.parent()
    });
  }

var dummy_data = [
  {
    "id": 1,
    "full_name": "Galen Slixby",
    "role": "Editor",
    "username": "gslixby0",
    "email": "gslixby0@abc.net.au",
    "current_plan": "Enterprise",
    "billing": "Manual - Credit Card",
    "status": 3,
    "avatar": ""
  },
  {
    "id": 2,
    "full_name": "Halsey Redmore",
    "role": "Author",
    "username": "hredmore1",
    "email": "hredmore1@imgur.com",
    "current_plan": "Team",
    "billing": "Manual - Paypal",
    "status": 1,
    "avatar": ""
  },
  {
    "id": 3,
    "full_name": "Marjory Sicely",
    "role": "Maintainer",
    "username": "msicely2",
    "email": "msicely2@who.int",
    "current_plan": "Enterprise",
    "billing": "Auto Debit",
    "status": 2,
    "avatar": ""
  },
  {
    "id": 4,
    "full_name": "Cyrill Risby",
    "role": "Maintainer",
    "username": "crisby3",
    "email": "crisby3@wordpress.com",
    "current_plan": "Team",
    "billing": "Manual - Credit Card",
    "status": 3,
    "avatar": ""
  },
  {
    "id": 5,
    "full_name": "Maggy Hurran",
    "role": "Subscriber",
    "username": "mhurran4",
    "email": "mhurran4@yahoo.co.jp",
    "current_plan": "Enterprise",
    "billing": "Auto Debit",
    "status": 1,
    "avatar": ""
  },
  {
    "id": 6,
    "full_name": "Silvain Halstead",
    "role": "Author",
    "username": "shalstead5",
    "email": "shalstead5@shinystat.com",
    "current_plan": "Company",
    "billing": "Auto Debit",
    "status": 2,
    "avatar": ""
  },
  {
    "id": 7,
    "full_name": "Breena Gallemore",
    "role": "Subscriber",
    "username": "bgallemore6",
    "email": "bgallemore6@boston.com",
    "current_plan": "Company",
    "billing": "Manual - Paypal",
    "status": 1,
    "avatar": ""
  },
  {
    "id": 8,
    "full_name": "Kathryne Liger",
    "role": "Author",
    "username": "kliger7",
    "email": "kliger7@vinaora.com",
    "current_plan": "Enterprise",
    "billing": "Manual - Cash",
    "status": 1,
    "avatar": ""
  },
  {
    "id": 9,
    "full_name": "Franz Scotfurth",
    "role": "Subscriber",
    "username": "fscotfurth8",
    "email": "fscotfurth8@dailymotion.com",
    "current_plan": "Team",
    "billing": "Auto Debit",
    "status": 1,
    "avatar": ""
  },
  {
    "id": 10,
    "full_name": "Jillene Bellany",
    "role": "Maintainer",
    "username": "jbellany9",
    "email": "jbellany9@kickstarter.com",
    "current_plan": "Company",
    "billing": "Auto Debit",
    "status": 3,
    "avatar": ""
  },
  {
    "id": 11,
    "full_name": "Jonah Wharlton",
    "role": "Subscriber",
    "username": "jwharltona",
    "email": "jwharltona@oakley.com",
    "current_plan": "Team",
    "billing": "Manual - Paypal",
    "status": 3,
    "avatar": ""
  },
  {
    "id": 12,
    "full_name": "Seth Hallam",
    "role": "Subscriber",
    "username": "shallamb",
    "email": "shallamb@hugedomains.com",
    "current_plan": "Team",
    "billing": "Manual - Credit Card",
    "status": 1,
    "avatar": ""
  },
  {
    "id": 13,
    "full_name": "Yoko Pottie",
    "role": "Subscriber",
    "username": "ypottiec",
    "email": "ypottiec@privacy.gov.au",
    "current_plan": "Basic",
    "billing": "Auto Debit",
    "status": 3,
    "avatar": ""
  },
  {
    "id": 14,
    "full_name": "Maximilianus Krause",
    "role": "Author",
    "username": "mkraused",
    "email": "mkraused@stanford.edu",
    "current_plan": "Team",
    "billing": "Auto Debit",
    "status": 2,
    "avatar": ""
  },
  {
    "id": 15,
    "full_name": "Zsazsa McCleverty",
    "role": "Maintainer",
    "username": "zmcclevertye",
    "email": "zmcclevertye@soundcloud.com",
    "current_plan": "Enterprise",
    "billing": "Auto Debit",
    "status": 2,
    "avatar": ""
  },
  {
    "id": 16,
    "full_name": "Bentlee Emblin",
    "role": "Author",
    "username": "bemblinf",
    "email": "bemblinf@wired.com",
    "current_plan": "Company",
    "billing": "Auto Debit",
    "status": 2,
    "avatar": ""
  },
  {
    "id": 17,
    "full_name": "Brockie Myles",
    "role": "Maintainer",
    "username": "bmylesg",
    "email": "bmylesg@amazon.com",
    "current_plan": "Basic",
    "billing": "Manual - Paypal",
    "status": 2,
    "avatar": ""
  },
  {
    "id": 18,
    "full_name": "Bertha Biner",
    "role": "Editor",
    "username": "bbinerh",
    "email": "bbinerh@mozilla.com",
    "current_plan": "Team",
    "billing": "Manual - Cash",
    "status": 2,
    "avatar": ""
  },
  {
    "id": 19,
    "full_name": "Travus Bruntjen",
    "role": "Admin",
    "username": "tbruntjeni",
    "email": "tbruntjeni@sitemeter.com",
    "current_plan": "Enterprise",
    "billing": "Manual - Cash",
    "status": 2,
    "avatar": ""
  },
  {
    "id": 20,
    "full_name": "Wesley Burland",
    "role": "Editor",
    "username": "wburlandj",
    "email": "wburlandj@uiuc.edu",
    "current_plan": "Team",
    "billing": "Auto Debit",
    "status": 3,
    "avatar": ""
  },
  {
    "id": 21,
    "full_name": "Stu Delamaine",
    "role": "Author",
    "username": "sdelamainek",
    "email": "sdelamainek@who.int",
    "current_plan": "Basic",
    "billing": "Auto Debit",
    "status": 1,
    "avatar": ""
  },
  {
    "id": 22,
    "full_name": "Jameson Lyster",
    "role": "Editor",
    "username": "jlysterl",
    "email": "jlysterl@guardian.co.uk",
    "current_plan": "Company",
    "billing": "Auto Debit",
    "status": 3,
    "avatar": ""
  },
  {
    "id": 23,
    "full_name": "Kare Skitterel",
    "role": "Maintainer",
    "username": "kskitterelm",
    "email": "kskitterelm@washingtonpost.com",
    "current_plan": "Basic",
    "billing": "Manual - Paypal",
    "status": 1,
    "avatar": ""
  },
  {
    "id": 24,
    "full_name": "Cleavland Hatherleigh",
    "role": "Admin",
    "username": "chatherleighn",
    "email": "chatherleighn@washington.edu",
    "current_plan": "Team",
    "billing": "Manual - Paypal",
    "status": 1,
    "avatar": ""
  },
  {
    "id": 25,
    "full_name": "Adeline Micco",
    "role": "Admin",
    "username": "amiccoo",
    "email": "amiccoo@whitehouse.gov",
    "current_plan": "Enterprise",
    "billing": "Manual - Credit Card",
    "status": 1,
    "avatar": ""
  },
  {
    "id": 26,
    "full_name": "Hugh Hasson",
    "role": "Admin",
    "username": "hhassonp",
    "email": "hhassonp@bizjournals.com",
    "current_plan": "Basic",
    "billing": "Manual - Cash",
    "status": 3,
    "avatar": ""
  },
  {
    "id": 27,
    "full_name": "Germain Jacombs",
    "role": "Editor",
    "username": "gjacombsq",
    "email": "gjacombsq@jigsy.com",
    "current_plan": "Enterprise",
    "billing": "Manual - Cash",
    "status": 2,
    "avatar": ""
  },
  {
    "id": 28,
    "full_name": "Bree Kilday",
    "role": "Maintainer",
    "username": "bkildayr",
    "email": "bkildayr@mashable.com",
    "current_plan": "Team",
    "billing": "Manual - Credit Card",
    "status": 2,
    "avatar": ""
  },
  {
    "id": 29,
    "full_name": "Candice Pinyon",
    "role": "Maintainer",
    "username": "cpinyons",
    "email": "cpinyons@behance.net",
    "current_plan": "Team",
    "billing": "Auto Debit",
    "status": 2,
    "avatar": ""
  },
  {
    "id": 30,
    "full_name": "Isabel Mallindine",
    "role": "Subscriber",
    "username": "imallindinet",
    "email": "imallindinet@shinystat.com",
    "current_plan": "Team",
    "billing": "Manual - Credit Card",
    "status": 1,
    "avatar": ""
  },
  {
    "id": 31,
    "full_name": "Gwendolyn Meineken",
    "role": "Admin",
    "username": "gmeinekenu",
    "email": "gmeinekenu@hc360.com",
    "current_plan": "Basic",
    "billing": "Manual - Cash",
    "status": 1,
    "avatar": ""
  },
  {
    "id": 32,
    "full_name": "Rafaellle Snowball",
    "role": "Editor",
    "username": "rsnowballv",
    "email": "rsnowballv@indiegogo.com",
    "current_plan": "Basic",
    "billing": "Manual - Paypal",
    "status": 1,
    "avatar": ""
  },
  {
    "id": 33,
    "full_name": "Rochette Emer",
    "role": "Admin",
    "username": "remerw",
    "email": "remerw@blogtalkradio.com",
    "current_plan": "Basic",
    "billing": "Auto Debit",
    "status": 2,
    "avatar": ""
  },
  {
    "id": 34,
    "full_name": "Ophelie Fibbens",
    "role": "Subscriber",
    "username": "ofibbensx",
    "email": "ofibbensx@booking.com",
    "current_plan": "Company",
    "billing": "Manual - Cash",
    "status": 2,
    "avatar": ""
  },
  {
    "id": 35,
    "full_name": "Stephen MacGilfoyle",
    "role": "Maintainer",
    "username": "smacgilfoyley",
    "email": "smacgilfoyley@bigcartel.com",
    "current_plan": "Company",
    "billing": "Manual - Paypal",
    "status": 1,
    "avatar": ""
  },
  {
    "id": 36,
    "full_name": "Bradan Rosebotham",
    "role": "Subscriber",
    "username": "brosebothamz",
    "email": "brosebothamz@tripadvisor.com",
    "current_plan": "Team",
    "billing": "Manual - Paypal",
    "status": 3,
    "avatar": ""
  },
  {
    "id": 37,
    "full_name": "Skip Hebblethwaite",
    "role": "Admin",
    "username": "shebblethwaite10",
    "email": "shebblethwaite10@arizona.edu",
    "current_plan": "Company",
    "billing": "Manual - Cash",
    "status": 3,
    "avatar": ""
  },
  {
    "id": 38,
    "full_name": "Moritz Piccard",
    "role": "Maintainer",
    "username": "mpiccard11",
    "email": "mpiccard11@vimeo.com",
    "current_plan": "Enterprise",
    "billing": "Manual - Credit Card",
    "status": 3,
    "avatar": ""
  },
  {
    "id": 39,
    "full_name": "Tyne Widmore",
    "role": "Subscriber",
    "username": "twidmore12",
    "email": "twidmore12@bravesites.com",
    "current_plan": "Team",
    "billing": "Manual - Cash",
    "status": 1,
    "avatar": ""
  },
  {
    "id": 40,
    "full_name": "Florenza Desporte",
    "role": "Author",
    "username": "fdesporte13",
    "email": "fdesporte13@omniture.com",
    "current_plan": "Company",
    "billing": "Manual - Cash",
    "status": 2,
    "avatar": ""
  },
  {
    "id": 41,
    "full_name": "Edwina Baldetti",
    "role": "Maintainer",
    "username": "ebaldetti14",
    "email": "ebaldetti14@theguardian.com",
    "current_plan": "Team",
    "billing": "Manual - Credit Card",
    "status": 1,
    "avatar": ""
  },
  {
    "id": 42,
    "full_name": "Benedetto Rossiter",
    "role": "Editor",
    "username": "brossiter15",
    "email": "brossiter15@craigslist.org",
    "current_plan": "Team",
    "billing": "Manual - Cash",
    "status": 3,
    "avatar": ""
  },
  {
    "id": 43,
    "full_name": "Micaela McNirlan",
    "role": "Admin",
    "username": "mmcnirlan16",
    "email": "mmcnirlan16@hc360.com",
    "current_plan": "Basic",
    "billing": "Manual - Credit Card",
    "status": 3,
    "avatar": ""
  },
  {
    "id": 44,
    "full_name": "Vladamir Koschek",
    "role": "Author",
    "username": "vkoschek17",
    "email": "vkoschek17@abc.net.au",
    "current_plan": "Team",
    "billing": "Manual - Paypal",
    "status": 2,
    "avatar": ""
  },
  {
    "id": 45,
    "full_name": "Corrie Perot",
    "role": "Subscriber",
    "username": "cperot18",
    "email": "cperot18@goo.ne.jp",
    "current_plan": "Team",
    "billing": "Manual - Paypal",
    "status": 1,
    "avatar": ""
  },
  {
    "id": 46,
    "full_name": "Saunder Offner",
    "role": "Maintainer",
    "username": "soffner19",
    "email": "soffner19@mac.com",
    "current_plan": "Enterprise",
    "billing": "Auto Debit",
    "status": 1,
    "avatar": ""
  },
  {
    "id": 47,
    "full_name": "Karena Courtliff",
    "role": "Admin",
    "username": "kcourtliff1a",
    "email": "kcourtliff1a@bbc.co.uk",
    "current_plan": "Basic",
    "billing": "Manual - Paypal",
    "status": 2,
    "avatar": ""
  },
  {
    "id": 48,
    "full_name": "Onfre Wind",
    "role": "Admin",
    "username": "owind1b",
    "email": "owind1b@yandex.ru",
    "current_plan": "Basic",
    "billing": "Manual - Paypal",
    "status": 1,
    "avatar": ""
  },
  {
    "id": 49,
    "full_name": "Paulie Durber",
    "role": "Subscriber",
    "username": "pdurber1c",
    "email": "pdurber1c@gov.uk",
    "current_plan": "Team",
    "billing": "Manual - Cash",
    "status": 3,
    "avatar": ""
  },
  {
    "id": 50,
    "full_name": "Beverlie Krabbe",
    "role": "Editor",
    "username": "bkrabbe1d",
    "email": "bkrabbe1d@home.pl",
    "current_plan": "Company",
    "billing": "Auto Debit",
    "status": 2,
    "avatar": ""
  }
];

  // Users datatable
  if (dt_user_table.length) {
    var dt_user = dt_user_table.DataTable({
      data: dummy_data,
      columns: [
        // columns according to JSON
        { data: '' },
        { data: 'full_name' },
        { data: 'role' },
        { data: 'current_plan' },
        { data: 'billing' },
        { data: 'status' },
        { data: 'action' }
      ],
      columnDefs: [
        {
          // For Responsive
          className: 'control',
          searchable: false,
          orderable: false,
          responsivePriority: 2,
          targets: 0,
          render: function (data, type, full, meta) {
            return '';
          }
        },
        {
          // User full name and email
          targets: 1,
          responsivePriority: 4,
          render: function (data, type, full, meta) {
            var $name = full['full_name'],
              $email = full['email'],
              $image = full['avatar'];
            if ($image) {
              // For Avatar image
              var $output =
                '<img src="' + assetsPath + 'img/avatars/' + $image + '" alt="Avatar" class="rounded-circle">';
            } else {
              // For Avatar badge
              var stateNum = Math.floor(Math.random() * 6);
              var states = ['success', 'danger', 'warning', 'info', 'primary', 'secondary'];
              var $state = states[stateNum],
                $name = full['full_name'],
                $initials = $name.match(/\b\w/g) || [];
              $initials = (($initials.shift() || '') + ($initials.pop() || '')).toUpperCase();
              $output = '<span class="avatar-initial rounded-circle bg-label-' + $state + '">' + $initials + '</span>';
            }
            // Creates full output for row
            var $row_output =
              '<div class="d-flex justify-content-start align-items-center user-name">' +
              '<div class="avatar-wrapper">' +
              '<div class="avatar avatar-sm me-3">' +
              $output +
              '</div>' +
              '</div>' +
              '<div class="d-flex flex-column">' +
              '<a href="' +
              userView +
              '" class="text-body text-truncate"><span class="fw-semibold">' +
              $name +
              '</span></a>' +
              '<small class="text-muted">' +
              $email +
              '</small>' +
              '</div>' +
              '</div>';
            return $row_output;
          }
        },
        {
          // User Role
          targets: 2,
          render: function (data, type, full, meta) {
            var $role = full['role'];
            var roleBadgeObj = {
              Subscriber:
                '<span class="badge badge-center rounded-pill bg-label-warning w-px-30 h-px-30 me-2"><i class="ti ti-user ti-sm"></i></span>',
              Author:
                '<span class="badge badge-center rounded-pill bg-label-success w-px-30 h-px-30 me-2"><i class="ti ti-circle-check ti-sm"></i></span>',
              Maintainer:
                '<span class="badge badge-center rounded-pill bg-label-primary w-px-30 h-px-30 me-2"><i class="ti ti-chart-pie-2 ti-sm"></i></span>',
              Editor:
                '<span class="badge badge-center rounded-pill bg-label-info w-px-30 h-px-30 me-2"><i class="ti ti-edit ti-sm"></i></span>',
              Admin:
                '<span class="badge badge-center rounded-pill bg-label-secondary w-px-30 h-px-30 me-2"><i class="ti ti-device-laptop ti-sm"></i></span>'
            };
            return "<span class='text-truncate d-flex align-items-center'>" + roleBadgeObj[$role] + $role + '</span>';
          }
        },
        {
          // Plans
          targets: 3,
          render: function (data, type, full, meta) {
            var $plan = full['current_plan'];

            return '<span class="fw-semibold">' + $plan + '</span>';
          }
        },
        {
          // User Status
          targets: 5,
          render: function (data, type, full, meta) {
            var $status = full['status'];

            return (
              '<span class="badge ' +
              statusObj[$status].class +
              '" text-capitalized>' +
              statusObj[$status].title +
              '</span>'
            );
          }
        },
        {
          // Actions
          targets: -1,
          title: 'Actions',
          searchable: false,
          orderable: false,
          render: function (data, type, full, meta) {
            return (
              '<div class="d-flex align-items-center">' +
              '<a href="javascript:;" class="text-body"><i class="ti ti-edit ti-sm me-2"></i></a>' +
              '<a href="javascript:;" class="text-body delete-record"><i class="ti ti-trash ti-sm mx-2"></i></a>' +
              '<a href="javascript:;" class="text-body dropdown-toggle hide-arrow" data-bs-toggle="dropdown"><i class="ti ti-dots-vertical ti-sm mx-1"></i></a>' +
              '<div class="dropdown-menu dropdown-menu-end m-0">' +
              '<a href="' +
              userView +
              '" class="dropdown-item">View</a>' +
              '<a href="javascript:;" class="dropdown-item">Suspend</a>' +
              '</div>' +
              '</div>'
            );
          }
        }
      ],
      order: [[1, 'desc']],
      dom:
        '<"row me-2"' +
        '<"col-md-2"<"me-3"l>>' +
        '<"col-md-10"<"dt-action-buttons text-xl-end text-lg-start text-md-end text-start d-flex align-items-center justify-content-end flex-md-row flex-column mb-3 mb-md-0"fB>>' +
        '>t' +
        '<"row mx-2"' +
        '<"col-sm-12 col-md-6"i>' +
        '<"col-sm-12 col-md-6"p>' +
        '>',
      language: {
        sLengthMenu: '_MENU_',
        search: '',
        searchPlaceholder: 'Search..'
      },
      // Buttons with Dropdown
      buttons: [
        {
          extend: 'collection',
          className: 'btn btn-label-secondary dropdown-toggle mx-3',
          text: '<i class="ti ti-screen-share me-1 ti-xs"></i>Export',
          buttons: [
            {
              extend: 'print',
              text: '<i class="ti ti-printer me-2" ></i>Print',
              className: 'dropdown-item',
              exportOptions: {
                columns: [1, 2, 3, 4, 5],
                // prevent avatar to be print
                format: {
                  body: function (inner, coldex, rowdex) {
                    if (inner.length <= 0) return inner;
                    var el = $.parseHTML(inner);
                    var result = '';
                    $.each(el, function (index, item) {
                      if (item.classList !== undefined && item.classList.contains('user-name')) {
                        result = result + item.lastChild.firstChild.textContent;
                      } else if (item.innerText === undefined) {
                        result = result + item.textContent;
                      } else result = result + item.innerText;
                    });
                    return result;
                  }
                }
              },
              customize: function (win) {
                //customize print view for dark
                $(win.document.body)
                  .css('color', headingColor)
                  .css('border-color', borderColor)
                  .css('background-color', bodyBg);
                $(win.document.body)
                  .find('table')
                  .addClass('compact')
                  .css('color', 'inherit')
                  .css('border-color', 'inherit')
                  .css('background-color', 'inherit');
              }
            },
            {
              extend: 'csv',
              text: '<i class="ti ti-file-text me-2" ></i>Csv',
              className: 'dropdown-item',
              exportOptions: {
                columns: [1, 2, 3, 4, 5],
                // prevent avatar to be display
                format: {
                  body: function (inner, coldex, rowdex) {
                    if (inner.length <= 0) return inner;
                    var el = $.parseHTML(inner);
                    var result = '';
                    $.each(el, function (index, item) {
                      if (item.classList !== undefined && item.classList.contains('user-name')) {
                        result = result + item.lastChild.firstChild.textContent;
                      } else if (item.innerText === undefined) {
                        result = result + item.textContent;
                      } else result = result + item.innerText;
                    });
                    return result;
                  }
                }
              }
            },
            {
              extend: 'excel',
              text: 'Excel',
              className: 'dropdown-item',
              exportOptions: {
                columns: [1, 2, 3, 4, 5],
                // prevent avatar to be display
                format: {
                  body: function (inner, coldex, rowdex) {
                    if (inner.length <= 0) return inner;
                    var el = $.parseHTML(inner);
                    var result = '';
                    $.each(el, function (index, item) {
                      if (item.classList !== undefined && item.classList.contains('user-name')) {
                        result = result + item.lastChild.firstChild.textContent;
                      } else if (item.innerText === undefined) {
                        result = result + item.textContent;
                      } else result = result + item.innerText;
                    });
                    return result;
                  }
                }
              }
            },
            {
              extend: 'pdf',
              text: '<i class="ti ti-file-code-2 me-2"></i>Pdf',
              className: 'dropdown-item',
              exportOptions: {
                columns: [1, 2, 3, 4, 5],
                // prevent avatar to be display
                format: {
                  body: function (inner, coldex, rowdex) {
                    if (inner.length <= 0) return inner;
                    var el = $.parseHTML(inner);
                    var result = '';
                    $.each(el, function (index, item) {
                      if (item.classList !== undefined && item.classList.contains('user-name')) {
                        result = result + item.lastChild.firstChild.textContent;
                      } else if (item.innerText === undefined) {
                        result = result + item.textContent;
                      } else result = result + item.innerText;
                    });
                    return result;
                  }
                }
              }
            },
            {
              extend: 'copy',
              text: '<i class="ti ti-copy me-2" ></i>Copy',
              className: 'dropdown-item',
              exportOptions: {
                columns: [1, 2, 3, 4, 5],
                // prevent avatar to be display
                format: {
                  body: function (inner, coldex, rowdex) {
                    if (inner.length <= 0) return inner;
                    var el = $.parseHTML(inner);
                    var result = '';
                    $.each(el, function (index, item) {
                      if (item.classList !== undefined && item.classList.contains('user-name')) {
                        result = result + item.lastChild.firstChild.textContent;
                      } else if (item.innerText === undefined) {
                        result = result + item.textContent;
                      } else result = result + item.innerText;
                    });
                    return result;
                  }
                }
              }
            }
          ]
        },
        {
          text: '<i class="ti ti-plus me-0 me-sm-1 ti-xs"></i><span class="d-none d-sm-inline-block">Add New User</span>',
          className: 'add-new btn btn-primary',
          attr: {
            'data-bs-toggle': 'offcanvas',
            'data-bs-target': '#offcanvasAddUser'
          }
        }
      ],
      // For responsive popup
      responsive: {
        details: {
          display: $.fn.dataTable.Responsive.display.modal({
            header: function (row) {
              var data = row.data();
              return 'Details of ' + data['full_name'];
            }
          }),
          type: 'column',
          renderer: function (api, rowIdx, columns) {
            var data = $.map(columns, function (col, i) {
              return col.title !== '' // ? Do not show row in modal popup if title is blank (for check box)
                ? '<tr data-dt-row="' +
                    col.rowIndex +
                    '" data-dt-column="' +
                    col.columnIndex +
                    '">' +
                    '<td>' +
                    col.title +
                    ':' +
                    '</td> ' +
                    '<td>' +
                    col.data +
                    '</td>' +
                    '</tr>'
                : '';
            }).join('');

            return data ? $('<table class="table"/><tbody />').append(data) : false;
          }
        }
      },
      initComplete: function () {
        // Adding role filter once table initialized
        this.api()
          .columns(2)
          .every(function () {
            var column = this;
            var select = $(
              '<select id="UserRole" class="form-select text-capitalize"><option value=""> Select Role </option></select>'
            )
              .appendTo('.user_role')
              .on('change', function () {
                var val = $.fn.dataTable.util.escapeRegex($(this).val());
                column.search(val ? '^' + val + '$' : '', true, false).draw();
              });

            column
              .data()
              .unique()
              .sort()
              .each(function (d, j) {
                select.append('<option value="' + d + '">' + d + '</option>');
              });
          });
        // Adding plan filter once table initialized
        this.api()
          .columns(3)
          .every(function () {
            var column = this;
            var select = $(
              '<select id="UserPlan" class="form-select text-capitalize"><option value=""> Select Plan </option></select>'
            )
              .appendTo('.user_plan')
              .on('change', function () {
                var val = $.fn.dataTable.util.escapeRegex($(this).val());
                column.search(val ? '^' + val + '$' : '', true, false).draw();
              });

            column
              .data()
              .unique()
              .sort()
              .each(function (d, j) {
                select.append('<option value="' + d + '">' + d + '</option>');
              });
          });
        // Adding status filter once table initialized
        this.api()
          .columns(5)
          .every(function () {
            var column = this;
            var select = $(
              '<select id="FilterTransaction" class="form-select text-capitalize"><option value=""> Select Status </option></select>'
            )
              .appendTo('.user_status')
              .on('change', function () {
                var val = $.fn.dataTable.util.escapeRegex($(this).val());
                column.search(val ? '^' + val + '$' : '', true, false).draw();
              });

            column
              .data()
              .unique()
              .sort()
              .each(function (d, j) {
                select.append(
                  '<option value="' +
                    statusObj[d].title +
                    '" class="text-capitalize">' +
                    statusObj[d].title +
                    '</option>'
                );
              });
          });
      }
    });
  }

  // Delete Record
  $('.datatables-users tbody').on('click', '.delete-record', function () {
    dt_user.row($(this).parents('tr')).remove().draw();
  });

  // Filter form control to default size
  // ? setTimeout used for multilingual table initialization
  setTimeout(() => {
    $('.dataTables_filter .form-control').removeClass('form-control-sm');
    $('.dataTables_length .form-select').removeClass('form-select-sm');
  }, 300);
});

// Validation & Phone mask
(function () {
  const phoneMaskList = document.querySelectorAll('.phone-mask'),
    addNewUserForm = document.getElementById('addNewUserForm');

  // Phone Number
  if (phoneMaskList) {
    phoneMaskList.forEach(function (phoneMask) {
      new Cleave(phoneMask, {
        phone: true,
        phoneRegionCode: 'US'
      });
    });
  }
  // Add New User Form Validation
  const fv = FormValidation.formValidation(addNewUserForm, {
    fields: {
      userFullname: {
        validators: {
          notEmpty: {
            message: 'Please enter fullname '
          }
        }
      },
      userEmail: {
        validators: {
          notEmpty: {
            message: 'Please enter your email'
          },
          emailAddress: {
            message: 'The value is not a valid email address'
          }
        }
      }
    },
    plugins: {
      trigger: new FormValidation.plugins.Trigger(),
      bootstrap5: new FormValidation.plugins.Bootstrap5({
        // Use this for enabling/changing valid/invalid class
        eleValidClass: '',
        rowSelector: function (field, ele) {
          // field is the field name & ele is the field element
          return '.mb-3';
        }
      }),
      submitButton: new FormValidation.plugins.SubmitButton(),
      // Submit the form when all fields are valid
      // defaultSubmit: new FormValidation.plugins.DefaultSubmit(),
      autoFocus: new FormValidation.plugins.AutoFocus()
    }
  });
})();
