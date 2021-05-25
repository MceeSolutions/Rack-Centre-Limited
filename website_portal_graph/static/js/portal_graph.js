var rpc;
var session;
var myChart;
var myLabels = [];
var myDatas = [];
var myColors = [];
odoo.define('website_portal_graph.sale_portal_graph', function (require) {
	"use strict";
	rpc = require('web.rpc');
	session = require('web.session');
});

$(document).ready(function () {
	var url = window.location.pathname;
	var type;
	if (window.location.href.indexOf("/my/quotes") > -1) {
		type = 'Sales Analysis'
		var doc_quote_table = $('.o_portal_my_doc_table');
		var graph_view = $('.graph_view');
		var graph_quote = $('.graph_quotation');
		var list_button = $('.list_quotation');
		var sort_by = $('#list_sort_by')
		var graph_option = $("#graph_options");
		var start_date = $(".start_date");
		var end_date = $(".end_date");
		var group_by = $("#group_by_quotation");
		var filter_option = $("select#filter_by_quotation");
		var month_seperator = $('a.month_seperator');
		var year_seperator = $('a.year_seperator');
		var bar = $("button.bar_graph");
		var line = $("button.line_graph");
		var pie = $("button.pie_graph");
		var doughnut = $("button.doughnut_graph");
		var polar = $("button.polar_graph");
		var filter = $(".fliter_by_quotation")
		var reset = $(".reset_button_quote");
		var default_view = $(".no_group_quote");

		list_button.css('background', 'black');
		graph_option.hide()
		graph_view.hide()
		filter.hide()
		bar.addClass("active_graph");

		list_button.click(function () {
			list_button.css('background', 'black')
			graph_quote.css('background', '#00A09D')
			sort_by.show();
			graph_option.hide()
			graph_view.hide();
			doc_quote_table.show()
			$(".o_portal_pager").show()
		})
		graph_quote.click(function () {
			if (group_by.val()) {
				graph_option.show();
			} else {
				graph_option.hide();
			}
			graph_quote.css('background', 'black')
			list_button.css('background', '#00A09D')
			sort_by.hide();
			graph_view.show();
			doc_quote_table.hide()
			$(".o_portal_pager").hide()
		})

		bar.click(function () {
			bar.addClass("active_graph");
			line.removeClass("active_graph");
			pie.removeClass("active_graph");
			doughnut.removeClass("active_graph");
			polar.removeClass("active_graph");
			bar_graph();
		})
		line.click(function () {
			line.addClass("active_graph");
			bar.removeClass("active_graph");
			pie.removeClass("active_graph");
			doughnut.removeClass("active_graph");
			polar.removeClass("active_graph");
			line_graph();
		})
		pie.click(function () {
			pie.addClass("active_graph");
			bar.removeClass("active_graph");
			line.removeClass("active_graph");
			doughnut.removeClass("active_graph");
			polar.removeClass("active_graph");
			pie_graph();
		})
		doughnut.click(function () {
			doughnut.addClass("active_graph");
			bar.removeClass("active_graph");
			line.removeClass("active_graph");
			pie.removeClass("active_graph");
			polar.removeClass("active_graph");
			doughnut_graph();
		})
		polar.click(function () {
			polar.addClass("active_graph");
			bar.removeClass("active_graph");
			line.removeClass("active_graph");
			pie.removeClass("active_graph");
			doughnut.removeClass("active_graph");
			polar_graph();
		})

		month_seperator.click(function () {
			month_seperator.addClass("last_active");
			year_seperator.removeClass("last_active");
			var start_date = $('#start_date').val();
			var end_date = $('#end_date').val();
			var valid_start_date = new Date($('#start_date').val());
			var valid_end_date = new Date($('#end_date').val());
			if (valid_start_date <= valid_end_date) {
				if (filter_option.val() == 'cancelled') {
					filter_option.change();
				} else {
					rpc.query({
						model: 'sale.order',
						method: 'get_quotation_values_by_date',
						args: [, session.user_id, start_date, end_date, 'month'],
					}).then(function (values) {
						if (values) {
							var my_length = values['my_labels'].length;
							var i = 0;
							var rgb = [];
							for (var k = 0; k < my_length; k++) {
								var rgb_val = [];
								var rgb_vals = [];
								for (i = 0; i < 3; i++) {
									rgb_vals.push(Math.floor(Math.random() * 255));
								}
								var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
								rgb_val += rgb_val_joined;
								rgb.push(rgb_val);
							}
							myColors = rgb;
							myLabels = values['my_labels'];
							myDatas = values['my_data'];
							var l = line.hasClass("active_graph");
							var pi = pie.hasClass("active_graph");
							var d = doughnut.hasClass("active_graph");
							var p = polar.hasClass("active_graph");
							if (l) {
								line_graph()
							} else if (pi) {
								pie_graph()
							} else if (d) {
								doughnut_graph()
							} else if (p) {
								polar_graph()
							} else {
								bar_graph()
							}
						} else {
							$("canvas#bar-chart-front").hide();
							$.confirm({
								title: 'Error',
								content: 'Record Does not exits',
							});
						}
					});
				}
			} else {
				$.confirm({
					title: 'Error',
					content: 'Please ! Enter Valid Date',
				});
			}
		})

		year_seperator.click(function () {
			month_seperator.removeClass("last_active");
			year_seperator.addClass("last_active");
			var start_date = $('#start_date').val();
			var end_date = $('#end_date').val();
			var valid_start_date = new Date($('#start_date').val());
			var valid_end_date = new Date($('#end_date').val());
			if (valid_start_date <= valid_end_date) {
				if (filter_option.val() == 'cancelled') {
					filter_option.change();
				} else {
					rpc.query({
						model: 'sale.order',
						method: 'get_quotation_values_by_year',
						args: [, session.user_id, start_date, end_date, 'year'],
					}).then(function (values) {
						if (values) {
							var my_length = values['my_labels'].length;
							var i = 0;
							var rgb = [];
							for (var k = 0; k < my_length; k++) {
								var rgb_val = [];
								var rgb_vals = [];
								for (i = 0; i < 3; i++) {
									rgb_vals.push(Math.floor(Math.random() * 255));
								}
								var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
								rgb_val += rgb_val_joined;
								rgb.push(rgb_val);
							}
							myColors = rgb;
							myLabels = values['my_labels'];
							myDatas = values['my_data'];
							var l = line.hasClass("active_graph");
							var pi = pie.hasClass("active_graph");
							var d = doughnut.hasClass("active_graph");
							var p = polar.hasClass("active_graph");
							if (l) {
								line_graph()
							} else if (pi) {
								pie_graph()
							} else if (d) {
								doughnut_graph()
							} else if (p) {
								polar_graph()
							} else {
								bar_graph()
							}
						} else {
							$("canvas#bar-chart-front").hide();
							$.confirm({
								title: 'Error',
								content: 'Record Not Found',
							});
						}
					});
				}
			} else {
				$.confirm({
					title: 'Error',
					content: 'Please ! Enter Valid Date',
				});
			}
		});

		group_by.change(function () {
			var val = $(this).children("option:selected").val();
			if (myChart) {
				myChart.destroy();
			}
			if (val == 'customer') {
				reset.removeClass('d-none')
				filter.show();
				default_view.hide();
				graph_option.show();
				start_date.addClass("d-none");
				end_date.addClass("d-none");
				$("#filter_by_quotation").val(false)
				rpc.query({
					model: 'sale.order',
					method: 'get_quotation_values',
					args: [, session.user_id],
				}).then(function (values) {
					if (values) {
						var my_length = values['my_labels'].length;
						var i = 0;
						var rgb = [];
						for (var k = 0; k < my_length; k++) {
							var rgb_val = [];
							var rgb_vals = [];
							for (i = 0; i < 3; i++) {
								rgb_vals.push(Math.floor(Math.random() * 255));
							}
							var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
							rgb_val += rgb_val_joined;
							rgb.push(rgb_val);
						}
						myColors = rgb;
						myLabels = values['my_labels'];
						myDatas = values['my_data'];
						var l = line.hasClass("active_graph");
						var pi = pie.hasClass("active_graph");
						var d = doughnut.hasClass("active_graph");
						var p = polar.hasClass("active_graph");
						if (l) {
							line_graph()
						} else if (pi) {
							pie_graph()
						} else if (d) {
							doughnut_graph()
						} else if (p) {
							polar_graph()
						} else {
							bar_graph()
						}
					} else {
						$("canvas#bar-chart-front").hide();
						$.confirm({
							title: 'Error',
							content: 'Record Does not exits',
						});
					}
				});
			} else if (val == 'month') {
				filter.show()
				reset.removeClass('d-none')
				start_date.removeClass("d-none");
				graph_option.show();
				default_view.hide();
				$("#start_date").val(false);
				$("#end_date").val(false);
				month_seperator.removeClass("last_active");
				year_seperator.removeClass("last_active");
				end_date.removeClass("d-none");
				$("#filter_by_quotation").val(false)
				rpc.query({
					model: 'sale.order',
					method: 'get_quotation_month_values',
					args: [, session.user_id],
				}).then(function (values) {
					if (values) {
						var my_length = values['my_labels'].length;
						var i = 0;
						var rgb = [];
						for (var k = 0; k < my_length; k++) {
							var rgb_val = [];
							var rgb_vals = [];
							for (i = 0; i < 3; i++) {
								rgb_vals.push(Math.floor(Math.random() * 255));
							}
							var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
							rgb_val += rgb_val_joined;
							rgb.push(rgb_val);
						}
						myColors = rgb;
						myLabels = values['my_labels'];
						myDatas = values['my_data']
						var l = line.hasClass("active_graph");
						var pi = pie.hasClass("active_graph");
						var d = doughnut.hasClass("active_graph");
						var p = polar.hasClass("active_graph");
						if (l) {
							line_graph()
						} else if (pi) {
							pie_graph()
						} else if (d) {
							doughnut_graph()
						} else if (p) {
							polar_graph()
						} else {
							bar_graph()
						}
					} else {
						$("canvas#bar-chart-front").hide();
						$.confirm({
							title: 'Error',
							content: 'Record Does not exits',
						});
					}
				});
			} else {
				graph_option.hide();
				default_view.show();
				filter.hide();
				start_date.addClass("d-none");
				end_date.addClass("d-none");
				reset.addClass('d-none')
			}
		})

		filter_option.change(function () {
			var val = group_by.children("option:selected").val();
			var sel_val = $(this).children("option:selected").val();
			if (val == 'customer') {
				if (sel_val === 'cancelled') {
					rpc.query({
						model: 'sale.order',
						method: 'get_customer_quotation_cancelled_values',
						args: [, session.user_id],
					}).then(function (values) {
						if (values) {
							var my_length = values['my_labels'].length;
							var i = 0;
							var rgb = [];
							for (var k = 0; k < my_length; k++) {
								var rgb_val = [];
								var rgb_vals = [];
								for (i = 0; i < 3; i++) {
									rgb_vals.push(Math.floor(Math.random() * 255));
								}
								var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
								rgb_val += rgb_val_joined;
								rgb.push(rgb_val);
							}
							myColors = rgb;
							myLabels = values['my_labels'];
							myDatas = values['my_data']
							var l = line.hasClass("active_graph");
							var pi = pie.hasClass("active_graph");
							var d = doughnut.hasClass("active_graph");
							var p = polar.hasClass("active_graph");
							if (l) {
								line_graph()
							} else if (pi) {
								pie_graph()
							} else if (d) {
								doughnut_graph()
							} else if (p) {
								polar_graph()
							} else {
								bar_graph()
							}
						} else {
							$("canvas#bar-chart-front").hide();
							$.confirm({
								title: 'Error',
								content: 'Record Does not exits',
							});
						}
					});
				} else {
					group_by.change();
				}
			} else if (val == 'month') {
				if (sel_val === 'cancelled') {
					var m = month_seperator.hasClass("last_active")
					var y = year_seperator.hasClass("last_active")
					if (y) {
						var start_date = $('#start_date').val();
						var end_date = $('#end_date').val();
						rpc.query({
							model: 'sale.order',
							method: 'get_quotation_cancelled_values_year',
							args: [, session.user_id, start_date, end_date],
						}).then(function (values) {
							if (values) {
								var my_length = values['my_labels'].length;
								var i = 0;
								var rgb = [];
								for (var k = 0; k < my_length; k++) {
									var rgb_val = [];
									var rgb_vals = [];
									for (i = 0; i < 3; i++) {
										rgb_vals.push(Math.floor(Math.random() * 255));
									}
									var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
									rgb_val += rgb_val_joined;
									rgb.push(rgb_val);
								}
								myColors = rgb;
								myLabels = values['my_labels'];
								myDatas = values['my_data']
								var l = line.hasClass("active_graph");
								var pi = pie.hasClass("active_graph");
								var d = doughnut.hasClass("active_graph");
								var p = polar.hasClass("active_graph");
								if (l) {
									line_graph()
								} else if (pi) {
									pie_graph()
								} else if (d) {
									doughnut_graph()
								} else if (p) {
									polar_graph()
								} else {
									bar_graph()
								}
							} else {
								$("canvas#bar-chart-front").hide();
								$.confirm({
									title: 'Error',
									content: 'Record Does not exits',
								});
							}
						});
					} else if (m) {
						var start_date = $('#start_date').val();
						var end_date = $('#end_date').val();
						rpc.query({
							model: 'sale.order',
							method: 'get_quotation_cancelled_values_month',
							args: [, session.user_id, start_date, end_date],
						}).then(function (values) {
							if (values) {
								var my_length = values['my_labels'].length;
								var i = 0;
								var rgb = [];
								for (var k = 0; k < my_length; k++) {
									var rgb_val = [];
									var rgb_vals = [];
									for (i = 0; i < 3; i++) {
										rgb_vals.push(Math.floor(Math.random() * 255));
									}
									var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
									rgb_val += rgb_val_joined;
									rgb.push(rgb_val);
								}
								myColors = rgb;
								myLabels = values['my_labels'];
								myDatas = values['my_data']
								var l = line.hasClass("active_graph");
								var pi = pie.hasClass("active_graph");
								var d = doughnut.hasClass("active_graph");
								var p = polar.hasClass("active_graph");
								if (l) {
									line_graph()
								} else if (pi) {
									pie_graph()
								} else if (d) {
									doughnut_graph()
								} else if (p) {
									polar_graph()
								} else {
									bar_graph()
								}
							} else {
								$("canvas#bar-chart-front").hide();
								$.confirm({
									title: 'Error',
									content: 'Record Does not exits',
								});
							}
						});
					} else {
						rpc.query({
							model: 'sale.order',
							method: 'get_quotation_cancelled_values',
							args: [, session.user_id],
						}).then(function (values) {
							if (values) {
								var my_length = values['my_labels'].length;
								var i = 0;
								var rgb = [];
								for (var k = 0; k < my_length; k++) {
									var rgb_val = [];
									var rgb_vals = [];
									for (i = 0; i < 3; i++) {
										rgb_vals.push(Math.floor(Math.random() * 255));
									}
									var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
									rgb_val += rgb_val_joined;
									rgb.push(rgb_val);
								}
								myColors = rgb;
								myLabels = values['my_labels'];
								myDatas = values['my_data']
								var l = line.hasClass("active_graph");
								var pi = pie.hasClass("active_graph");
								var d = doughnut.hasClass("active_graph");
								var p = polar.hasClass("active_graph");
								if (l) {
									line_graph()
								} else if (pi) {
									pie_graph()
								} else if (d) {
									doughnut_graph()
								} else if (p) {
									polar_graph()
								} else {
									bar_graph()
								}
							} else {
								$("canvas#bar-chart-front").hide();
								$.confirm({
									title: 'Error',
									content: 'Record Does not exits',
								});
							}
						});
					}
				} else {
					var mc = month_seperator.hasClass("last_active");
					var yc = year_seperator.hasClass("last_active");
					if (yc) {
						if (sel_val == 'default') {
							year_seperator.click()
						}
					} else if (mc) {
						if (sel_val == 'default') {
							month_seperator.click()
						}
					} else {
						rpc.query({
							model: 'sale.order',
							method: 'get_quotation_month_values',
							args: [, session.user_id],
						}).then(function (values) {
							if (values) {
								var my_length = values['my_labels'].length;
								var i = 0;
								var rgb = [];
								for (var k = 0; k < my_length; k++) {
									var rgb_val = [];
									var rgb_vals = [];
									for (i = 0; i < 3; i++) {
										rgb_vals.push(Math.floor(Math.random() * 255));
									}
									var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
									rgb_val += rgb_val_joined;
									rgb.push(rgb_val);
								}
								myColors = rgb;
								myLabels = values['my_labels'];
								myDatas = values['my_data'];
								var l = line.hasClass("active_graph");
								var pi = pie.hasClass("active_graph");
								var d = doughnut.hasClass("active_graph");
								var p = polar.hasClass("active_graph");
								if (l) {
									line_graph()
								} else if (pi) {
									pie_graph()
								} else if (d) {
									doughnut_graph()
								} else if (p) {
									polar_graph()
								} else {
									bar_graph()
								}
							} else {
								$("canvas#bar-chart-front").hide();
								$.confirm({
									title: 'Error',
									content: 'Record Does not exits',
								});
							}
						});
					}
				}
			}
		})

		$("#reset_button_quote").click(function () {
			$("#group_by_quotation").val(false);
			group_by.change();
		})
	} else if (window.location.href.indexOf('/my/orders') > -1) {
		type = 'Sales Analysis';
		var doc_quote_table = $('.o_portal_my_doc_table');
		var graph_quote = $('.graph_view');
		var list_button = $('.list_orders');
		var graph_button = $('.graph_orders');
		var sort_by = $('#list_sort_by')
		var graph_option = $("#graph_options");
		var month = $("a.month_seperator");
		var year = $("a.year_seperator");
		var bar = $("button.bar_graph");
		var line = $("button.line_graph");
		var pie = $("button.pie_graph");
		var doughnut = $("button.doughnut_graph");
		var polar = $("button.polar_graph");
		var group_by = $("#group_by_order")
		var default_view = $(".no_group_order")
		var reset = $(".reset_button_order")

		list_button.css('background', 'black');
		bar.addClass("active_graph");
		graph_quote.hide();
		graph_option.hide()

		list_button.click(function () {
			list_button.css('background', 'black');
			graph_button.css('background', '#00A09D')
			doc_quote_table.show();
			sort_by.show();
			graph_quote.hide();
			graph_option.hide()
			$(".o_portal_pager").show()
		})
		graph_button.click(function () {
			graph_button.css('background', 'black')
			list_button.css('background', '#00A09D');
			doc_quote_table.hide();
			sort_by.hide();
			graph_quote.show();
			if (group_by.val()) {
				graph_option.show()
			} else {
				graph_option.hide()
			}
			$(".o_portal_pager").hide()
		})

		bar.click(function () {
			bar.addClass("active_graph");
			line.removeClass("active_graph");
			pie.removeClass("active_graph");
			doughnut.removeClass("active_graph");
			polar.removeClass("active_graph");
			bar_graph();
		})
		line.click(function () {
			line.addClass("active_graph");
			bar.removeClass("active_graph");
			pie.removeClass("active_graph");
			doughnut.removeClass("active_graph");
			polar.removeClass("active_graph");
			line_graph();
		})
		pie.click(function () {
			pie.addClass("active_graph");
			bar.removeClass("active_graph");
			line.removeClass("active_graph");
			doughnut.removeClass("active_graph");
			polar.removeClass("active_graph");
			pie_graph();
		})
		doughnut.click(function () {
			doughnut.addClass("active_graph");
			bar.removeClass("active_graph");
			line.removeClass("active_graph");
			pie.removeClass("active_graph");
			polar.removeClass("active_graph");
			doughnut_graph();
		})
		polar.click(function () {
			polar.addClass("active_graph");
			bar.removeClass("active_graph");
			line.removeClass("active_graph");
			pie.removeClass("active_graph");
			doughnut.removeClass("active_graph");
			polar_graph();
		})

		month.click(function () {
			var start_date = $("input#start_date").val();
			var end_date = $("input#end_date").val();
			var valid_start_date = new Date($('#start_date').val());
			var valid_end_date = new Date($('#end_date').val());
			if (valid_start_date <= valid_end_date) {
				rpc.query({
					model: 'sale.order',
					method: 'get_order_values_by_date',
					args: [, session.user_id, start_date, end_date],
				}).then(function (values) {
					if (values) {
						var my_length = values['my_labels'].length;
						var i = 0;
						var rgb = [];
						for (var k = 0; k < my_length; k++) {
							var rgb_val = [];
							var rgb_vals = [];
							for (i = 0; i < 3; i++) {
								rgb_vals.push(Math.floor(Math.random() * 255));
							}
							var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
							rgb_val += rgb_val_joined;
							rgb.push(rgb_val);
						}
						myColors = rgb;
						myLabels = values['my_labels'];
						myDatas = values['my_data'];
						var l = line.hasClass("active_graph");
						var pi = pie.hasClass("active_graph");
						var d = doughnut.hasClass("active_graph");
						var p = polar.hasClass("active_graph");
						if (l) {
							line_graph()
						} else if (pi) {
							pie_graph()
						} else if (d) {
							doughnut_graph()
						} else if (p) {
							polar_graph()
						} else {
							bar_graph()
						}
					} else {
						$("canvas#bar-chart-front").hide();
						$.confirm({
							title: 'Error',
							content: 'Record Does not exits',
						});
					}
				});
			} else {
				$.confirm({
					title: 'Error',
					content: 'Please ! Enter Valid Date',
				});
			}
		})

		year.click(function () {
			var start_date = $("input#start_date").val();
			var end_date = $("input#end_date").val();
			var valid_start_date = new Date($('#start_date').val());
			var valid_end_date = new Date($('#end_date').val());
			if (valid_start_date <= valid_end_date) {
				rpc.query({
					model: 'sale.order',
					method: 'get_order_values_by_year',
					args: [, session.user_id, start_date, end_date],
				}).then(function (values) {
					if (values) {
						var my_length = values['my_labels'].length;
						var i = 0;
						var rgb = [];
						for (var k = 0; k < my_length; k++) {
							var rgb_val = [];
							var rgb_vals = [];
							for (i = 0; i < 3; i++) {
								rgb_vals.push(Math.floor(Math.random() * 255));
							}
							var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
							rgb_val += rgb_val_joined;
							rgb.push(rgb_val);
						}
						myColors = rgb;
						myLabels = values['my_labels'];
						myDatas = values['my_data'];
						var l = line.hasClass("active_graph");
						var pi = pie.hasClass("active_graph");
						var d = doughnut.hasClass("active_graph");
						var p = polar.hasClass("active_graph");
						if (l) {
							line_graph()
						} else if (pi) {
							pie_graph()
						} else if (d) {
							doughnut_graph()
						} else if (p) {
							polar_graph()
						} else {
							bar_graph()
						}
					} else {
						$("canvas#bar-chart-front").hide();
						$.confirm({
							title: 'Error',
							content: 'Record Not Found',
						});
					}
				});
			} else {
				$.confirm({
					title: 'Error',
					content: 'Please ! Enter Valid Date',
				});
			}
		});

		group_by.change(function () {
			var val = $(this).children("option:selected").val();
			if (myChart) {
				myChart.destroy();
			}
			if (val == 'customer') {
				$(".start_date").addClass("d-none");
				$(".end_date").addClass("d-none");
				default_view.hide()
				reset.removeClass("d-none")
				graph_option.show()
				rpc.query({
					model: 'sale.order',
					method: 'get_customer_order_values',
					args: [, session.user_id],
				}).then(function (values) {
					if (values) {
						var my_length = values['my_labels'].length;
						var i = 0;
						var rgb = [];
						for (var k = 0; k < my_length; k++) {
							var rgb_val = [];
							var rgb_vals = [];
							for (i = 0; i < 3; i++) {
								rgb_vals.push(Math.floor(Math.random() * 255));
							}
							var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
							rgb_val += rgb_val_joined;
							rgb.push(rgb_val);
						}
						myColors = rgb;
						myLabels = values['my_labels'];
						myDatas = values['my_data'];
						var l = line.hasClass("active_graph");
						var pi = pie.hasClass("active_graph");
						var d = doughnut.hasClass("active_graph");
						var p = polar.hasClass("active_graph");
						if (l) {
							line_graph()
						} else if (pi) {
							pie_graph()
						} else if (d) {
							doughnut_graph()
						} else if (p) {
							polar_graph()
						} else {
							bar_graph()
						}
					} else {
						$("canvas#bar-chart-front").hide();
						$.confirm({
							title: 'Error',
							content: 'Record Does not exits',
						});
					}
				});
			} else if (val == 'month') {
				$(".start_date").removeClass("d-none")
				$(".end_date").removeClass("d-none")
				default_view.hide()
				$("#start_date").val(false)
				$("#end_date").val(false)
				reset.removeClass("d-none")
				graph_option.show()
				rpc.query({
					model: 'sale.order',
					method: 'get_month_order_values',
					args: [, session.user_id],
				}).then(function (values) {
					if (values) {
						var my_length = values['my_labels'].length;
						var i = 0;
						var rgb = [];
						for (var k = 0; k < my_length; k++) {
							var rgb_val = [];
							var rgb_vals = [];
							for (i = 0; i < 3; i++) {
								rgb_vals.push(Math.floor(Math.random() * 255));
							}
							var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
							rgb_val += rgb_val_joined;
							rgb.push(rgb_val);
						}
						myColors = rgb;
						myLabels = values['my_labels'];
						myDatas = values['my_data'];
						var l = line.hasClass("active_graph");
						var pi = pie.hasClass("active_graph");
						var d = doughnut.hasClass("active_graph");
						var p = polar.hasClass("active_graph");
						if (l) {
							line_graph()
						} else if (pi) {
							pie_graph()
						} else if (d) {
							doughnut_graph()
						} else if (p) {
							polar_graph()
						} else {
							bar_graph()
						}
					} else {
						$("canvas#bar-chart-front").hide();
						$.confirm({
							title: 'Error',
							content: 'Record Does not exits',
						});
					}
				});
			} else {
				$(".start_date").addClass("d-none");
				$(".end_date").addClass("d-none");
				default_view.show()
				graph_option.hide()
				reset.addClass("d-none")
			}
		})

		$("#reset_button_order").click(function () {
			$("#group_by_order").val(false)
			group_by.change();
		})
	} else if (window.location.href.indexOf('/my/invoices') > -1) {
		type = 'Invoice Analysis';
		var list_button = $(".list_invoices");
		var graph_button = $(".graph_invoices");
		var doc_quote_table = $('.o_portal_my_doc_table');
		var graph_quote = $(".graph_view");
		var sort_by = $('#list_sort_by')
		var graph_option = $("#graph_options");
		var bar = $("button.bar_graph");
		var line = $("button.line_graph");
		var pie = $("button.pie_graph");
		var doughnut = $("button.doughnut_graph");
		var polar = $("button.polar_graph");
		var group_by = $("select#group_by_invoice")
		var default_view = $(".no_group_invoice")
		var customer_filter = $("div.filter_by_customer_invoice");
		var date_filter = $("div.filter_by_date_invoice");
		var reset = $("div.reset_button_invoice")
		var start_date = $(".start_date");
		var end_date = $(".end_date");
		var month_seperator = $('a.month_seperator');
		var year_seperator = $('a.year_seperator');

		list_button.css("background", "black");
		graph_option.hide();
		graph_quote.hide();
		bar.addClass("active_graph");

		list_button.click(function () {
			graph_button.css("background", "#00A09D")
			list_button.css("background", "black")
			doc_quote_table.show();
			graph_quote.hide();
			sort_by.show();
			graph_option.hide();
			$(".o_portal_pager").show()
		})

		graph_button.click(function () {
			graph_button.css("background", "black")
			list_button.css("background", "#00A09D")
			doc_quote_table.hide();
			graph_quote.show();
			sort_by.hide();
			if (group_by.val()) {
				graph_option.show();
			} else {
				graph_option.hide();
			}
			$(".o_portal_pager").hide()
		})

		bar.click(function () {
			bar.addClass("active_graph");
			line.removeClass("active_graph");
			pie.removeClass("active_graph");
			doughnut.removeClass("active_graph");
			polar.removeClass("active_graph");
			bar_graph();
		})
		line.click(function () {
			line.addClass("active_graph");
			bar.removeClass("active_graph");
			pie.removeClass("active_graph");
			doughnut.removeClass("active_graph");
			polar.removeClass("active_graph");
			line_graph();
		})
		pie.click(function () {
			pie.addClass("active_graph");
			bar.removeClass("active_graph");
			line.removeClass("active_graph");
			doughnut.removeClass("active_graph");
			polar.removeClass("active_graph");
			pie_graph();
		})
		doughnut.click(function () {
			doughnut.addClass("active_graph");
			bar.removeClass("active_graph");
			line.removeClass("active_graph");
			pie.removeClass("active_graph");
			polar.removeClass("active_graph");
			doughnut_graph();
		})
		polar.click(function () {
			polar.addClass("active_graph");
			bar.removeClass("active_graph");
			line.removeClass("active_graph");
			pie.removeClass("active_graph");
			doughnut.removeClass("active_graph");
			polar_graph();
		})

		month_seperator.click(function () {
			month_seperator.addClass("last_active");
			year_seperator.removeClass("last_active");
			var start_date = $('#start_date').val();
			var end_date = $('#end_date').val();
			var valid_start_date = new Date($('#start_date').val());
			var valid_end_date = new Date($('#end_date').val());
			if (valid_start_date <= valid_end_date) {
				rpc.query({
					model: 'account.move',
					method: 'get_invoice_values_by_year_month',
					args: [, session.user_id, start_date, end_date, 'month', false],
				}).then(function (values) {
					if (values) {
						var my_length = values['my_labels'].length;
						var i = 0;
						var rgb = [];
						for (var k = 0; k < my_length; k++) {
							var rgb_val = [];
							var rgb_vals = [];
							for (i = 0; i < 3; i++) {
								rgb_vals.push(Math.floor(Math.random() * 255));
							}
							var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
							rgb_val += rgb_val_joined;
							rgb.push(rgb_val);
						}
						myColors = rgb;
						myLabels = values['my_labels'];
						myDatas = values['my_data'];
						var l = line.hasClass("active_graph");
						var pi = pie.hasClass("active_graph");
						var d = doughnut.hasClass("active_graph");
						var p = polar.hasClass("active_graph");
						if (l) {
							line_graph()
						} else if (pi) {
							pie_graph()
						} else if (d) {
							doughnut_graph()
						} else if (p) {
							polar_graph()
						} else {
							bar_graph()
						}
					} else {
						$("canvas#bar-chart-front").hide();
						$.confirm({
							title: 'Error',
							content: 'Record Does not exits',
						});
					}
				})
			} else {
				$.confirm({
					title: 'Error',
					content: 'Please ! Enter Valid Date',
				});
			}
		})

		year_seperator.click(function () {
			month_seperator.removeClass("last_active");
			year_seperator.addClass("last_active");
			var start_date = $('#start_date').val();
			var end_date = $('#end_date').val();
			var valid_start_date = new Date($('#start_date').val());
			var valid_end_date = new Date($('#end_date').val());
			if (valid_start_date <= valid_end_date) {
				rpc.query({
					model: 'account.move',
					method: 'get_invoice_values_by_year_month',
					args: [, session.user_id, start_date, end_date, 'year', false],
				}).then(function (values) {
					if (values) {
						var my_length = values['my_labels'].length;
						var i = 0;
						var rgb = [];
						for (var k = 0; k < my_length; k++) {
							var rgb_val = [];
							var rgb_vals = [];
							for (i = 0; i < 3; i++) {
								rgb_vals.push(Math.floor(Math.random() * 255));
							}
							var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
							rgb_val += rgb_val_joined;
							rgb.push(rgb_val);
						}
						myColors = rgb;
						myLabels = values['my_labels'];
						myDatas = values['my_data'];
						var l = line.hasClass("active_graph");
						var pi = pie.hasClass("active_graph");
						var d = doughnut.hasClass("active_graph");
						var p = polar.hasClass("active_graph");
						if (l) {
							line_graph()
						} else if (pi) {
							pie_graph()
						} else if (d) {
							doughnut_graph()
						} else if (p) {
							polar_graph()
						} else {
							bar_graph()
						}
					} else {
						$("canvas#bar-chart-front").hide();
						$.confirm({
							title: 'Error',
							content: 'Record Does not exits',
						});
					}
				})
			} else {
				$.confirm({
					title: 'Error',
					content: 'Please ! Enter Valid Date',
				});
			}
		})

		group_by.change(function () {
			var val = $(this).children("option:selected").val();
			if (myChart) {
				myChart.destroy();
			}
			if (val == 'customer') {
				default_view.hide()
				graph_option.show();
				customer_filter.removeClass('d-none')
				date_filter.addClass('d-none')
				reset.removeClass("d-none")
				start_date.addClass("d-none")
				end_date.addClass("d-none")
				$("#filter_by_customer_invoice").val(false)
				rpc.query({
					model: 'account.move',
					method: 'get_customer_invoice_values',
					args: [, session.user_id, 'customer'],
				}).then(function (values) {
					if (values) {
						var my_length = values['my_labels'].length;
						var i = 0;
						var rgb = [];
						for (var k = 0; k < my_length; k++) {
							var rgb_val = [];
							var rgb_vals = [];
							for (i = 0; i < 3; i++) {
								rgb_vals.push(Math.floor(Math.random() * 255));
							}
							var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
							rgb_val += rgb_val_joined;
							rgb.push(rgb_val);
						}
						myColors = rgb;
						myLabels = values['my_labels'];
						myDatas = values['my_data'];
						var l = line.hasClass("active_graph");
						var pi = pie.hasClass("active_graph");
						var d = doughnut.hasClass("active_graph");
						var p = polar.hasClass("active_graph");
						if (l) {
							line_graph()
						} else if (pi) {
							pie_graph()
						} else if (d) {
							doughnut_graph()
						} else if (p) {
							polar_graph()
						} else {
							bar_graph()
						}
					} else {
						$("canvas#bar-chart-front").hide();
						$.confirm({
							title: 'Error',
							content: 'Record Does not exits',
						});
					}
				});
			} else if (val == 'date') {
				start_date.removeClass("d-none")
				end_date.removeClass("d-none")
				reset.removeClass("d-none")
				default_view.hide()
				graph_option.show();
				customer_filter.addClass('d-none')
				$("#start_date").val(false);
				$("#end_date").val(false);
				$("#filter_by_date_invoice").val(false);
				date_filter.removeClass('d-none')
				year_seperator.removeClass("last_active");
				month_seperator.removeClass("last_active");
				rpc.query({
					model: 'account.move',
					method: 'get_invocie_date_values',
					args: [, session.user_id, 'default'],
				}).then(function (values) {
					if (values) {
						var my_length = values['my_labels'].length;
						var i = 0;
						var rgb = [];
						for (var k = 0; k < my_length; k++) {
							var rgb_val = [];
							var rgb_vals = [];
							for (i = 0; i < 3; i++) {
								rgb_vals.push(Math.floor(Math.random() * 255));
							}
							var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
							rgb_val += rgb_val_joined;
							rgb.push(rgb_val);
						}
						myColors = rgb;
						myLabels = values['my_labels'];
						myDatas = values['my_data']
						var l = line.hasClass("active_graph");
						var pi = pie.hasClass("active_graph");
						var d = doughnut.hasClass("active_graph");
						var p = polar.hasClass("active_graph");
						if (l) {
							line_graph()
						} else if (pi) {
							pie_graph()
						} else if (d) {
							doughnut_graph()
						} else if (p) {
							polar_graph()
						} else {
							bar_graph()
						}
					} else {
						$("canvas#bar-chart-front").hide();
						$.confirm({
							title: 'Error',
							content: 'Record Does not exits',
						});
					}
				});
			} else {
				start_date.addClass("d-none")
				end_date.addClass("d-none")
				reset.addClass("d-none")
				default_view.show()
				graph_option.hide();
				customer_filter.addClass('d-none')
				date_filter.addClass('d-none')
			}
		})

		$("#filter_by_customer_invoice").change(function () {
			var sel_val = $(this).children("option:selected").val();
			if (sel_val == 'open') {
				rpc.query({
					model: 'account.move',
					method: 'get_customer_invoice_values',
					args: [, session.user_id, 'open'],
				}).then(function (values) {
					if (values) {
						var my_length = values['my_labels'].length;
						var i = 0;
						var rgb = [];
						for (var k = 0; k < my_length; k++) {
							var rgb_val = [];
							var rgb_vals = [];
							for (i = 0; i < 3; i++) {
								rgb_vals.push(Math.floor(Math.random() * 255));
							}
							var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
							rgb_val += rgb_val_joined;
							rgb.push(rgb_val);
						}
						myColors = rgb;
						myLabels = values['my_labels'];
						myDatas = values['my_data'];
						var l = line.hasClass("active_graph");
						var pi = pie.hasClass("active_graph");
						var d = doughnut.hasClass("active_graph");
						var p = polar.hasClass("active_graph");
						if (l) {
							line_graph()
						} else if (pi) {
							pie_graph()
						} else if (d) {
							doughnut_graph()
						} else if (p) {
							polar_graph()
						} else {
							bar_graph()
						}
					} else {
						$("canvas#bar-chart-front").hide();
						$.confirm({
							title: 'Error',
							content: 'Record Does not exits',
						});
					}
				})
			} else if (sel_val == 'paid') {
				rpc.query({
					model: 'account.move',
					method: 'get_customer_invoice_values',
					args: [, session.user_id, 'paid'],
				}).then(function (values) {
					if (values) {
						var my_length = values['my_labels'].length;
						var i = 0;
						var rgb = [];
						for (var k = 0; k < my_length; k++) {
							var rgb_val = [];
							var rgb_vals = [];
							for (i = 0; i < 3; i++) {
								rgb_vals.push(Math.floor(Math.random() * 255));
							}
							var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
							rgb_val += rgb_val_joined;
							rgb.push(rgb_val);
						}
						myColors = rgb;
						myLabels = values['my_labels'];
						myDatas = values['my_data'];
						var l = line.hasClass("active_graph");
						var pi = pie.hasClass("active_graph");
						var d = doughnut.hasClass("active_graph");
						var p = polar.hasClass("active_graph");
						if (l) {
							line_graph()
						} else if (pi) {
							pie_graph()
						} else if (d) {
							doughnut_graph()
						} else if (p) {
							polar_graph()
						} else {
							bar_graph()
						}
					} else {
						$("canvas#bar-chart-front").hide();
						$.confirm({
							title: 'Error',
							content: 'Record Does not exits',
						});
					}
				})
			} else if (sel_val == 'due') {
				rpc.query({
					model: 'account.move',
					method: 'get_customer_due_invoice_values',
					args: [, session.user_id],
				}).then(function (values) {
					if (values) {
						var my_length = values['my_labels'].length;
						var i = 0;
						var rgb = [];
						for (var k = 0; k < my_length; k++) {
							var rgb_val = [];
							var rgb_vals = [];
							for (i = 0; i < 3; i++) {
								rgb_vals.push(Math.floor(Math.random() * 255));
							}
							var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
							rgb_val += rgb_val_joined;
							rgb.push(rgb_val);
						}
						myColors = rgb;
						myLabels = values['my_labels'];
						myDatas = values['my_data'];
						var l = line.hasClass("active_graph");
						var pi = pie.hasClass("active_graph");
						var d = doughnut.hasClass("active_graph");
						var p = polar.hasClass("active_graph");
						if (l) {
							line_graph()
						} else if (pi) {
							pie_graph()
						} else if (d) {
							doughnut_graph()
						} else if (p) {
							polar_graph()
						} else {
							bar_graph()
						}
					} else {
						$("canvas#bar-chart-front").hide();
						$.confirm({
							title: 'Error',
							content: 'Record Does not exits',
						});
					}
				})
			} else {
				group_by.change();
			}
		})

		$("#filter_by_date_invoice").click(function () {
			var sel_val = $("select#filter_by_date_invoice").children("option:selected").val();
			var start_date = $('#start_date').val();
			var end_date = $('#end_date').val();
			var month_c = month_seperator.hasClass("last_active");
			var year_c = year_seperator.hasClass("last_active");
			if (month_c) {
				if (sel_val == 'open') {
					rpc.query({
						model: 'account.move',
						method: 'get_invoice_values_by_year_month',
						args: [, session.user_id, start_date, end_date, 'month', 'open'],
					}).then(function (values) {
						if (values) {
							var my_length = values['my_labels'].length;
							var i = 0;
							var rgb = [];
							for (var k = 0; k < my_length; k++) {
								var rgb_val = [];
								var rgb_vals = [];
								for (i = 0; i < 3; i++) {
									rgb_vals.push(Math.floor(Math.random() * 255));
								}
								var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
								rgb_val += rgb_val_joined;
								rgb.push(rgb_val);
							}
							myColors = rgb;
							myLabels = values['my_labels'];
							myDatas = values['my_data'];
							var l = line.hasClass("active_graph");
							var pi = pie.hasClass("active_graph");
							var d = doughnut.hasClass("active_graph");
							var p = polar.hasClass("active_graph");
							if (l) {
								line_graph()
							} else if (pi) {
								pie_graph()
							} else if (d) {
								doughnut_graph()
							} else if (p) {
								polar_graph()
							} else {
								bar_graph()
							}
						} else {
							$("canvas#bar-chart-front").hide();
							$.confirm({
								title: 'Error',
								content: 'Record Does not exits',
							});
						}
					})
				} else if (sel_val == 'paid') {
					rpc.query({
						model: 'account.move',
						method: 'get_invoice_values_by_year_month',
						args: [, session.user_id, start_date, end_date, 'month', 'paid'],
					}).then(function (values) {
						if (values) {
							var my_length = values['my_labels'].length;
							var i = 0;
							var rgb = [];
							for (var k = 0; k < my_length; k++) {
								var rgb_val = [];
								var rgb_vals = [];
								for (i = 0; i < 3; i++) {
									rgb_vals.push(Math.floor(Math.random() * 255));
								}
								var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
								rgb_val += rgb_val_joined;
								rgb.push(rgb_val);
							}
							myColors = rgb;
							myLabels = values['my_labels'];
							myDatas = values['my_data'];
							var l = line.hasClass("active_graph");
							var pi = pie.hasClass("active_graph");
							var d = doughnut.hasClass("active_graph");
							var p = polar.hasClass("active_graph");
							if (l) {
								line_graph()
							} else if (pi) {
								pie_graph()
							} else if (d) {
								doughnut_graph()
							} else if (p) {
								polar_graph()
							} else {
								bar_graph()
							}
						} else {
							$("canvas#bar-chart-front").hide();
							$.confirm({
								title: 'Error',
								content: 'Record Does not exits',
							});
						}
					})
				} else {
					month_seperator.click();
				}
			} else if (year_c) {
				if (sel_val == 'open') {
					rpc.query({
						model: 'account.move',
						method: 'get_invoice_values_by_year_month',
						args: [, session.user_id, start_date, end_date, 'year', 'open'],
					}).then(function (values) {
						if (values) {
							var my_length = values['my_labels'].length;
							var i = 0;
							var rgb = [];
							for (var k = 0; k < my_length; k++) {
								var rgb_val = [];
								var rgb_vals = [];
								for (i = 0; i < 3; i++) {
									rgb_vals.push(Math.floor(Math.random() * 255));
								}
								var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
								rgb_val += rgb_val_joined;
								rgb.push(rgb_val);
							}
							myColors = rgb;
							myLabels = values['my_labels'];
							myDatas = values['my_data'];
							var l = line.hasClass("active_graph");
							var pi = pie.hasClass("active_graph");
							var d = doughnut.hasClass("active_graph");
							var p = polar.hasClass("active_graph");
							if (l) {
								line_graph()
							} else if (pi) {
								pie_graph()
							} else if (d) {
								doughnut_graph()
							} else if (p) {
								polar_graph()
							} else {
								bar_graph()
							}
						} else {
							$("canvas#bar-chart-front").hide();
							$.confirm({
								title: 'Error',
								content: 'Record Does not exits',
							});
						}
					})
				} else if (sel_val == 'paid') {
					rpc.query({
						model: 'account.move',
						method: 'get_invoice_values_by_year_month',
						args: [, session.user_id, start_date, end_date, 'year', 'paid'],
					}).then(function (values) {
						if (values) {
							var my_length = values['my_labels'].length;
							var i = 0;
							var rgb = [];
							for (var k = 0; k < my_length; k++) {
								var rgb_val = [];
								var rgb_vals = [];
								for (i = 0; i < 3; i++) {
									rgb_vals.push(Math.floor(Math.random() * 255));
								}
								var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
								rgb_val += rgb_val_joined;
								rgb.push(rgb_val);
							}
							myColors = rgb;
							myLabels = values['my_labels'];
							myDatas = values['my_data'];
							var l = line.hasClass("active_graph");
							var pi = pie.hasClass("active_graph");
							var d = doughnut.hasClass("active_graph");
							var p = polar.hasClass("active_graph");
							if (l) {
								line_graph()
							} else if (pi) {
								pie_graph()
							} else if (d) {
								doughnut_graph()
							} else if (p) {
								polar_graph()
							} else {
								bar_graph()
							}
						} else {
							$("canvas#bar-chart-front").hide();
							$.confirm({
								title: 'Error',
								content: 'Record Does not exits',
							});
						}
					})
				} else {
					year_seperator.click();
				}
			} else if (sel_val == 'open') {
				rpc.query({
					model: 'account.move',
					method: 'get_invocie_date_values',
					args: [, session.user_id, 'open'],
				}).then(function (values) {
					if (values) {
						var my_length = values['my_labels'].length;
						var i = 0;
						var rgb = [];
						for (var k = 0; k < my_length; k++) {
							var rgb_val = [];
							var rgb_vals = [];
							for (i = 0; i < 3; i++) {
								rgb_vals.push(Math.floor(Math.random() * 255));
							}
							var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
							rgb_val += rgb_val_joined;
							rgb.push(rgb_val);
						}
						myColors = rgb;
						myLabels = values['my_labels'];
						myDatas = values['my_data']
						var l = line.hasClass("active_graph");
						var pi = pie.hasClass("active_graph");
						var d = doughnut.hasClass("active_graph");
						var p = polar.hasClass("active_graph");
						if (l) {
							line_graph()
						} else if (pi) {
							pie_graph()
						} else if (d) {
							doughnut_graph()
						} else if (p) {
							polar_graph()
						} else {
							bar_graph()
						}
					} else {
						$("canvas#bar-chart-front").hide();
						$.confirm({
							title: 'Error',
							content: 'Record Does not exits',
						});
					}
				});
			} else if (sel_val == 'paid') {
				rpc.query({
					model: 'account.move',
					method: 'get_invocie_date_values',
					args: [, session.user_id, 'paid'],
				}).then(function (values) {
					if (values) {
						var my_length = values['my_labels'].length;
						var i = 0;
						var rgb = [];
						for (var k = 0; k < my_length; k++) {
							var rgb_val = [];
							var rgb_vals = [];
							for (i = 0; i < 3; i++) {
								rgb_vals.push(Math.floor(Math.random() * 255));
							}
							var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
							rgb_val += rgb_val_joined;
							rgb.push(rgb_val);
						}
						myColors = rgb;
						myLabels = values['my_labels'];
						myDatas = values['my_data']
						var l = line.hasClass("active_graph");
						var pi = pie.hasClass("active_graph");
						var d = doughnut.hasClass("active_graph");
						var p = polar.hasClass("active_graph");
						if (l) {
							line_graph()
						} else if (pi) {
							pie_graph()
						} else if (d) {
							doughnut_graph()
						} else if (p) {
							polar_graph()
						} else {
							bar_graph()
						}
					} else {
						$("canvas#bar-chart-front").hide();
						$.confirm({
							title: 'Error',
							content: 'Record Does not exits',
						});
					}
				});
			} else {
				group_by.change();
			}
		})
		$("#reset_button_invoice").click(function () {
			group_by.val(false);
			group_by.change();
		})
	}


	function bar_graph() {
		if (myChart) {
			myChart.destroy();
		}
		myChart = new Chart(document.getElementById('bar-chart-front'), {
			type: 'bar',
			data: {
				labels: myLabels,
				datasets: [{
					label: type,
					backgroundColor: myColors,
					data: myDatas,
				}]
			},
			options: {
				legend: {
					display: false
				},
				title: {
					display: true,
					text: type
				},
				scales: {
					yAxes: [{
						ticks: {
							beginAtZero: true
						}
					}]
				}
			}
		});
	}

	function pie_graph() {
		if (myChart) {
			myChart.destroy();
		}
		myChart = new Chart(document.getElementById('bar-chart-front'), {
			type: 'pie',
			data: {
				labels: myLabels,
				datasets: [{
					label: type,
					backgroundColor: myColors,
					data: myDatas,
				}]
			},
			options: {
				title: {
					display: true,
					text: type
				},
			}
		});
	}

	function line_graph() {
		if (myChart) {
			myChart.destroy();
		}
		myChart = new Chart(document.getElementById("bar-chart-front"), {
			type: 'line',
			data: {
				labels: myLabels,
				datasets: [{
					data: myDatas,
					label: type,
					borderColor: myColors[0],
					fill: false
				}, ]
			},
			options: {
				title: {
					display: true,
					text: type
				}
			}
		});
	}

	function doughnut_graph() {
		if (myChart) {
			myChart.destroy();
		}
		myChart = new Chart(document.getElementById('bar-chart-front'), {
			type: 'doughnut',
			data: {
				labels: myLabels,
				datasets: [{
					label: type,
					backgroundColor: myColors,
					data: myDatas,
				}]
			},
			options: {
				legend: {
					display: false
				},
				title: {
					display: true,
					text: type
				},
			}

		});
	}

	function polar_graph() {
		if (myChart) {
			myChart.destroy();
		}
		myChart = new Chart(document.getElementById('bar-chart-front'), {
			type: 'polarArea',
			data: {
				labels: myLabels,
				datasets: [{
					label: type,
					backgroundColor: myColors,
					data: myDatas,
				}]
			},
			options: {
				plugins: {
					filler: {
						propagate: true
					}
				},
				title: {
					display: true,
					text: type
				},
			}
		});
	}
});