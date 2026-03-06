from admin_tools_stats.models import DashboardStats

def create_default_stats():
    DashboardStats.objects.get_or_create(
        graph_key="bookings_per_day",
        model_app_name="bookings",
        model_name="Booking",
        date_field_name="created_at",
        operation_field_name="id",
        type_operation_field_name="Count",
        default_time_scale="days",
    )
    
    