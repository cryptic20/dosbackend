from users.models import *
from graphene_django.types import DjangoObjectType
import graphene
from graphene import relay


class AddressType(DjangoObjectType):
    class Meta:
        model = Address


class NotificationType(DjangoObjectType):
    # id = graphene.ID(source='pk')

    class Meta:
        model = UserNotification
        interfaces = (relay.Node,)


class UserSettingsType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = UserSettings
        interfaces = (relay.Node,)


class EventType(DjangoObjectType):
    class Meta:
        model = Event


class ScheduleType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = Schedule
        interfaces = (relay.Node,)

    next_event = graphene.DateTime()

    def resolve_next_event(self, info):
        return Schedule.next(self)


class PickUpType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = PickUpInfo
        interfaces = (relay.Node,)
        convert_choices_to_enum = False


class CompletedPickUpType(DjangoObjectType):
    class Meta:
        model = CompletedPickUp
        interfaces = (relay.Node, )


class Query(object):
    schedules = graphene.List(ScheduleType)
    notifications = graphene.List(NotificationType)
    pick_up_info = graphene.List(PickUpType)
    address = graphene.List(AddressType)
    completed_pickup = graphene.List(CompletedPickUpType)


class PickUpInput(graphene.InputObjectType):
    bin_type = graphene.String()
    lbs = graphene.Float()
    instructions = graphene.String()


class EventInput(graphene.InputObjectType):
    info = graphene.Field(PickUpInput)


class ScheduleInput(graphene.InputObjectType):
    start = graphene.DateTime(required=True)
    end = graphene.DateTime(required=False, default_value=None)
    repeat = graphene.String(required=False, default_value='')
    repeat_until = graphene.Date(required=False, default_value=None)
    event = graphene.Field(EventInput)


class CreateSchedule(graphene.Mutation):
    """Create a schedule for the pick up"""
    class Arguments:
        schedule_data = ScheduleInput(required=True)
    schedule = graphene.Field(ScheduleType)
    success = graphene.Boolean()

    def mutate(root, info, schedule_data=None):
        schedule_data.event.info['user'] = CustomUser.objects.get(pk=info.context.user.id)
        pickup_info = PickUpInfo.objects.create(**schedule_data.event.info)
        schedule = Schedule(
            user=CustomUser.objects.get(pk=info.context.user.id),
            event=Event.objects.create(info=pickup_info),
            start=schedule_data.start,
            end=schedule_data.end,
            repeat=schedule_data.repeat,
            repeat_until=schedule_data.repeat_until
        )
        schedule.save()
        return CreateSchedule(schedule=schedule, success=True)


class DeleteSchedule(graphene.Mutation):
    """ Delete schedule object """
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        Schedule.objects.filter(id=kwargs['id']).delete()
        return cls(success=True)


class CreatePickUp(graphene.Mutation):
    """Create a pick up information"""
    success = graphene.Boolean()  # success message

    class Arguments:
        bin_type = graphene.String(required=True)
        lbs = graphene.Float(required=True)
        instructions = graphene.String(required=False, default_value='')

    # The class attributes define the response of the mutation
    pick_up = graphene.Field(PickUpType)

    def mutate(root, info, **kwargs):
        pick_up = PickUpInfo(
            user=CustomUser.objects.get(pk=info.context.user.id),
            **kwargs)
        pick_up.save()
        return CreatePickUp(success=True, pick_up=pick_up)


class UpdatePickUp(graphene.Mutation):
    """ edit pick up object """
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)
        bin_type = graphene.String(required=False)
        lbs = graphene.Float(required=False)
        instructions = graphene.String(required=False)

    def mutate(root, info, **kwargs):
        PickUpInfo.objects.filter(pk=kwargs['id']).update(**kwargs)
        return UpdatePickUp(success=True)


class DeletePickUp(graphene.Mutation):
    """ Delete pick up object """
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        PickUpInfo.objects.filter(id=kwargs['id']).delete()
        return cls(success=True)


class DeleteNotification(graphene.Mutation):
    """ Delete the notification of a user"""
    success = graphene.Boolean()

    class Arguments:
        id = graphene.UUID(required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        UserNotification.objects.filter(id=kwargs['id']).delete()
        return cls(success=True)


class SeenNotification(graphene.Mutation):
    """ Set notification to seen """
    success = graphene.Boolean()

    class Arguments:
        id = graphene.UUID(required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        UserNotification.objects.filter(id=kwargs['id']).update(seen=True)
        return cls(success=True)


class EditUserSettings(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID()
        notify = graphene.Boolean()
        reminder = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        UserSettings.objects.filter(pk=kwargs['id']).update(**kwargs)
        return cls(success=True)


class AddressInput(graphene.InputObjectType):
    address_line1 = graphene.String()
    address_line2 = graphene.String()
    city = graphene.String()
    state = graphene.String()
    zip_code = graphene.String()
    country = graphene.String()


class CreateAddress(graphene.Mutation):
    """Create a schedule for the pick up"""
    class Arguments:
        address_input = AddressInput(required=True)
    address = graphene.Field(AddressType)
    success = graphene.Boolean()

    def mutate(root, info, address_input=None):
        address_input['user'] = CustomUser.objects.get(pk=info.context.user.id)
        address = Address(**address_input)
        address.save()
        return CreateAddress(address=address, success=True)


class EditAddress(graphene.Mutation):
    """ Edit address of a user """
    class Arguments:
        address_input = AddressInput()
    success = graphene.Boolean()
    address = graphene.Field(AddressType)

    def mutate(root, info, address_input=None):
        Address.objects.filter(user__id=info.context.user.id).update(**address_input)
        return EditAddress(success=True, address=Address.objects.get(user__id=info.context.user.id))


class Mutation(object):
    mark_notification = SeenNotification.Field()
    delete_notification = DeleteNotification.Field()
    create_pickup = CreatePickUp.Field()
    update_pickup = UpdatePickUp.Field()
    delete_pickup = DeletePickUp.Field()
    create_schedule = CreateSchedule.Field()
    delete_schedule = DeleteSchedule.Field()
    edit_user_settings = EditUserSettings.Field()
    create_address = CreateAddress.Field()
    edit_address = EditAddress.Field()