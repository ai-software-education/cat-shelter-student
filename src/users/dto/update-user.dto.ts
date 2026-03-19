import { PartialType } from '@nestjs/swagger';
import { CreateUserDto } from './create-user.dto';

// PartialType автоматически делает все поля из CreateUserDto необязательными (@IsOptional)
export class UpdateUserDto extends PartialType(CreateUserDto) {}